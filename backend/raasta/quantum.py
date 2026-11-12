"""Genuine Qiskit QAOA with statevector optimization and Aer measurement shots."""

import argparse
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from qiskit import QuantumCircuit, qasm2, transpile
from qiskit.circuit.library import DiagonalGate
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from scipy.optimize import minimize

from .energy import EnergyTable, build_energy_table, canonical_from_qiskit
from .evaluator import evaluate
from .exact import solve_exact
from .provenance import environment_metadata
from .scenarios import get_scenario, list_scenarios
from .schema import Scenario, SolverResult, selection_key, validate_budget


def build_circuit(table: EnergyTable, parameters: np.ndarray, p: int = 1) -> QuantumCircuit:
    """Parameters: gamma[0:p], beta[0:p]. qi encodes action xi."""
    if type(p) is not int or p not in (1, 2):
        raise ValueError("p must be 1 or 2")
    parameters = np.asarray(parameters, dtype=float)
    if parameters.shape != (2 * p,) or not np.all(np.isfinite(parameters)):
        raise ValueError("expected 2*p finite parameters")
    circuit = QuantumCircuit(6, name="lifeline_qaoa")
    circuit.h(range(6))
    for layer in range(p):
        phases = np.exp(-1j * parameters[layer] * table.energies / table.scale)
        circuit.append(DiagonalGate(phases), range(6))
        circuit.rx(2 * parameters[p + layer], range(6))
    return circuit


def result_from_counts(counts: dict[str, int], scenario: Scenario, budget: float,
                       diagnostics: dict, warnings: tuple[str, ...] = ()) -> SolverResult:
    """Evaluate only observed samples. Never substitute the exact optimum."""
    budget = validate_budget(budget)
    if not counts or any(type(value) is not int or value <= 0 for value in counts.values()):
        raise ValueError("measurement counts must be nonempty positive integers")
    decoded = {canonical_from_qiskit(bits): count for bits, count in counts.items()}
    shots = sum(decoded.values())
    if shots != diagnostics["shots"]:
        raise ValueError("counts do not sum to requested shots")
    evaluations = [evaluate(bits, scenario, budget) for bits in decoded]
    feasible = [e for e in evaluations if e.feasible]
    best = min(feasible, key=selection_key) if feasible else None
    # Classical reference is used only after observed sample selection, for comparison.
    exact = solve_exact(scenario, budget).evaluation
    details = dict(diagnostics)
    details.update({
        "raw_qiskit_counts": dict(sorted(counts.items())),
        "distribution": [{"bitstring": bits, "count": count, "probability": count / shots}
                         for bits, count in sorted(decoded.items())],
        "feasible_sample_rate": sum(decoded[e.bitstring] for e in feasible) / shots,
        "exact_optimum": exact.utility,
        "optimality_gap": exact.utility - best.utility if best else None,
        "gap_definition": "exact utility minus best feasible observed utility (absolute service-score units)",
    })
    return SolverResult(scenario.id, "qaoa", budget, "ok" if best else "no_feasible_sample",
                        best, details, warnings + (() if best else ("No feasible state was measured.",)))


def solve_qaoa(scenario: Scenario, budget: float | None = None, *, seed: int = 42,
               shots: int = 512, p: int = 1, maxiter: int = 60) -> SolverResult:
    start = perf_counter()
    budget = validate_budget(scenario.budget_default if budget is None else budget)
    for name, value, lower, upper in (("seed", seed, 0, 2**32 - 1), ("shots", shots, 1, 100_000),
                                       ("p", p, 1, 2), ("maxiter", maxiter, 8, 1000)):
        if type(value) is not int or not lower <= value <= upper:
            raise ValueError(f"{name} must be an integer in {lower}..{upper}")
    table = build_energy_table(scenario, budget)
    rng = np.random.default_rng(seed)
    initial = np.concatenate((rng.uniform(0, 2 * np.pi, p), rng.uniform(0, np.pi, p)))
    trace = []

    def expectation(parameters):
        state = Statevector.from_instruction(build_circuit(table, parameters, p))
        energy = float(np.dot(state.probabilities(), table.energies))
        trace.append({"evaluation": len(trace) + 1, "parameters": parameters.tolist(),
                      "expected_energy": energy, "scaled_expected_energy": energy / table.scale})
        return energy / table.scale

    optimized = minimize(expectation, initial, method="COBYLA",
                         options={"maxiter": maxiter, "rhobeg": 0.5, "tol": 1e-5})
    circuit = build_circuit(table, optimized.x, p)
    circuit.measure_all()
    # Force explicit one-/two-qubit gate synthesis rather than an opaque unitary.
    # u3/cx are standard qelib1 gates, so the evidence round-trips in strict QASM2.
    compiled = transpile(circuit, basis_gates=["u3", "cx"],
                         optimization_level=1, seed_transpiler=seed)
    simulator = AerSimulator(method="statevector", max_parallel_threads=1)
    measurement = simulator.run(compiled, shots=shots, seed_simulator=seed).result()
    if not measurement.success:
        raise RuntimeError(f"Aer execution failed: {measurement.status}")
    counts = {str(bits): int(count) for bits, count in measurement.get_counts().items()}
    operations = {str(key): int(value) for key, value in compiled.count_ops().items()}
    warnings = (
        "Synthetic six-action demonstration on a noiseless simulator; no quantum advantage claim.",
        "Hamiltonian construction enumerates all 64 states and scales exponentially.",
        "Single seeded optimizer start; best observed sample is not an expected-performance guarantee.",
    )
    if not optimized.success:
        warnings += (f"Optimizer did not report convergence: {optimized.message}",)
    result = result_from_counts(counts, scenario, budget, {
        "shots": shots, "seed": seed, "p": p, "maxiter": maxiter,
        "qubits": circuit.num_qubits, "depth": compiled.depth(),
        "gate_count": sum(value for key, value in operations.items() if key not in ("measure", "barrier")),
        "operation_counts": operations, "gate_basis": ["u3", "cx"],
        "parameters": {"gamma": optimized.x[:p].tolist(), "beta": optimized.x[p:].tolist()},
        "initial_parameters": initial.tolist(), "optimizer": "COBYLA",
        "optimizer_success": bool(optimized.success), "optimizer_message": str(optimized.message),
        "optimizer_evaluations": int(optimized.nfev), "optimizer_trace": trace,
        "objective_evaluation": "exact Qiskit Statevector expectation; no training shots",
        "measurement_backend": "Qiskit AerSimulator statevector, final sampled measurements",
        "measurement_success": bool(measurement.success),
        "energy_penalty": table.penalty, "minimum_positive_violation": table.minimum_positive_violation,
        "energy_scale": table.scale, "energy_bitstrings_qiskit_index_order": list(table.bitstrings),
        "energy_values": table.energies.tolist(),
        "expected_energy": float(optimized.fun * table.scale),
        "compiled_qasm2": qasm2.dumps(compiled),
        "logical_circuit": str(circuit.draw(output="text", fold=120)),
    }, warnings)
    result.diagnostics["runtime_ms"] = (perf_counter() - start) * 1000
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=[s.id for s in list_scenarios()], default="flood_baseline")
    parser.add_argument("--budget", type=float, default=9)
    parser.add_argument("--shots", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--p", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=60)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("output already exists; choose a new filename to preserve measured runs")
    try:
        scenario = get_scenario(args.scenario)
        result = solve_qaoa(scenario, args.budget, shots=args.shots, seed=args.seed, p=args.p, maxiter=args.maxiter)
    except ValueError as error:
        parser.error(str(error))
    payload = {"environment": environment_metadata(), "scenario": scenario.to_dict(), "result": result.to_dict()}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
        print(json.dumps({"output": str(args.output), "status": result.status,
                          "utility": result.to_dict()["utility"],
                          "feasible_sample_rate": result.diagnostics["feasible_sample_rate"],
                          "optimality_gap": result.diagnostics["optimality_gap"]}))
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
