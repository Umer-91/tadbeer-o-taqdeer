import json

import numpy as np
import pytest
from qiskit import QuantumCircuit, qasm2, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator

from raasta.energy import build_energy_table, canonical_from_qiskit
from raasta.evaluator import evaluate
from raasta.quantum import build_circuit, result_from_counts, solve_qaoa
from raasta.scenarios import get_scenario


def test_all_basis_states_measure_in_action_order():
    circuits = []
    for index in range(64):
        circuit = QuantumCircuit(6)
        for qubit in range(6):
            if index & (1 << qubit):
                circuit.x(qubit)
        circuit.measure_all()
        circuits.append(circuit)
    result = AerSimulator(max_parallel_threads=1).run(circuits, shots=8, seed_simulator=42).result()
    assert result.success
    for index in range(64):
        counts = result.get_counts(index)
        assert counts == {f"{index:06b}": 8}
        canonical = canonical_from_qiskit(next(iter(counts)))
        assert [i for i, bit in enumerate(canonical) if bit == "1"] == [i for i in range(6) if index & (1 << i)]


def test_phase_operator_and_mixer_match_independent_dense_calculation():
    table = build_energy_table(get_scenario("flood_baseline"), 9)
    gamma, beta = 1.3, 0.4
    circuit = build_circuit(table, np.array([gamma, beta]))
    assert circuit.num_qubits == 6
    assert circuit.count_ops() == {"h": 6, "diagonal": 1, "rx": 6}
    diagonal = next(instruction.operation for instruction in circuit.data if instruction.operation.name == "diagonal")
    phases = np.exp(-1j * gamma * table.energies / table.scale)
    assert np.allclose(Operator(diagonal).data, np.diag(phases))
    rx = np.array([[np.cos(beta), -1j * np.sin(beta)], [-1j * np.sin(beta), np.cos(beta)]])
    mixer = rx
    for _ in range(5):
        mixer = np.kron(mixer, rx)
    expected = mixer @ (phases / 8)
    actual = Statevector.from_instruction(circuit).data
    assert np.allclose(actual, expected)
    assert not np.allclose(np.abs(actual)**2, np.ones(64)/64)
    compiled = transpile(circuit, basis_gates=["rz", "sx", "x", "cx"], seed_transpiler=42)
    assert compiled.count_ops()["cx"] > 0
    assert Statevector.from_instruction(compiled).equiv(Statevector(actual))


def test_second_qaoa_layer_is_real_and_normalized():
    table = build_energy_table(get_scenario("bridge_blocked"), 6)
    circuit = build_circuit(table, [0.3, 0.7, 0.2, 0.4], p=2)
    assert circuit.count_ops()["diagonal"] == 2
    assert circuit.count_ops()["rx"] == 12
    assert sum(Statevector.from_instruction(circuit).probabilities()) == pytest.approx(1)


def test_no_feasible_samples_never_substitutes_exact():
    result = result_from_counts({"111111": 8}, get_scenario("flood_baseline"), 9, {"shots": 8})
    output = result.to_dict()
    assert output["status"] == "no_feasible_sample"
    assert all(output[field] is None for field in ("bitstring", "utility", "total_cost", "feasible", "metrics"))
    assert output["selected_actions"] == []
    assert output["diagnostics"]["feasible_sample_rate"] == 0
    assert output["diagnostics"]["optimality_gap"] is None
    assert output["diagnostics"]["exact_optimum"] == 96


def test_only_measured_feasible_sample_can_win():
    result = result_from_counts({"000000": 2, "000001": 3, "111111": 5},
                               get_scenario("flood_baseline"), 9, {"shots": 10})
    assert result.evaluation.bitstring == "100000"
    assert result.evaluation.utility == 13
    assert result.diagnostics["feasible_sample_rate"] == 0.5
    assert result.diagnostics["optimality_gap"] == 83


@pytest.mark.parametrize("counts,shots", [({}, 1), ({"000000": 0}, 0), ({"111": 1}, 1),
                                         ({"000000": -1}, 1), ({"000000": 1}, 2)])
def test_invalid_measurements_fail_visibly(counts, shots):
    with pytest.raises(ValueError):
        result_from_counts(counts, get_scenario("flood_baseline"), 9, {"shots": shots})


@pytest.mark.parametrize("kwargs", [{"shots": 0}, {"shots": True}, {"seed": -1}, {"p": 3},
                                   {"p": True}, {"maxiter": 1}, {"shots": 100001}])
def test_invalid_quantum_options(kwargs):
    with pytest.raises(ValueError):
        solve_qaoa(get_scenario("flood_baseline"), **kwargs)


def test_seeded_real_qaoa_smoke_and_reproducibility():
    scenario = get_scenario("flood_baseline")
    results = [solve_qaoa(scenario, shots=128, seed=42, maxiter=12) for _ in range(2)]
    first, second = results
    assert first.diagnostics["raw_qiskit_counts"] == second.diagnostics["raw_qiskit_counts"]
    assert first.diagnostics["parameters"] == second.diagnostics["parameters"]
    d = first.diagnostics
    assert d["measurement_success"]
    assert sum(d["raw_qiskit_counts"].values()) == 128
    assert sum(row["probability"] for row in d["distribution"]) == pytest.approx(1)
    assert len(d["optimizer_trace"]) == d["optimizer_evaluations"] <= 12
    assert d["qubits"] == 6 and d["depth"] > 1 and d["operation_counts"]["cx"] > 0
    replay = qasm2.loads(d["compiled_qasm2"])
    assert replay.num_qubits == 6
    parameters = d["parameters"]["gamma"] + d["parameters"]["beta"]
    logical = build_circuit(build_energy_table(scenario, 9), parameters)
    assert Statevector.from_instruction(replay.remove_final_measurements(inplace=False)).equiv(
        Statevector.from_instruction(logical))
    for row in d["distribution"]:
        assert len(row["bitstring"]) == 6 and row["count"] > 0
    if first.status == "ok":
        assert first.evaluation == evaluate(first.evaluation.bitstring, scenario, 9)
        assert first.evaluation.feasible
        assert first.evaluation.bitstring in {row["bitstring"] for row in d["distribution"]}
        assert d["optimality_gap"] >= 0
    else:
        assert first.evaluation is None
    json.dumps(first.to_dict(), allow_nan=False)
