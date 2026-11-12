"""Re-evaluate recorded results and replay quantum circuit evidence locally."""

import argparse
import hashlib
import json
from pathlib import Path

from qiskit import qasm2
from qiskit.quantum_info import Statevector

from raasta.energy import build_energy_table
from raasta.evaluator import evaluate
from raasta.exact import solve_exact
from raasta.quantum import build_circuit
from raasta.scenarios import get_scenario


def verify(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    source = Path(__file__).resolve().parents[1] / "backend" / "raasta"
    for name, digest in payload["environment"]["source_sha256"].items():
        if Path(name).name != name:
            raise ValueError("source filenames must not contain directory components")
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == digest, f"source changed: {name}"
    runs = [payload["result"]] if "result" in payload else [r[name] for r in payload["runs"]
                                                           for name in ("exact", "greedy", "qaoa") if name in r]
    for result in runs:
        scenario = get_scenario(result["scenario_id"])
        budget, details = result["budget"], result["diagnostics"]
        if result["status"] == "ok":
            evaluation = evaluate(result["bitstring"], scenario, budget)
            assert evaluation.feasible
            assert (evaluation.utility, evaluation.total_cost) == (result["utility"], result["total_cost"])
            assert list(evaluation.selected_actions) == result["selected_actions"]
            assert all(getattr(evaluation, name) == value for name, value in result["metrics"].items())
        if result["algorithm"] != "qaoa":
            continue
        assert sum(details["raw_qiskit_counts"].values()) == details["shots"]
        assert sum(item["count"] for item in details["distribution"]) == details["shots"]
        assert len({item["bitstring"] for item in details["distribution"]}) == len(details["distribution"])
        feasible_counts = 0
        feasible_utilities = []
        for item in details["distribution"]:
            evaluation = evaluate(item["bitstring"], scenario, budget)
            assert item["count"] == details["raw_qiskit_counts"][item["bitstring"][::-1]]
            assert item["probability"] == item["count"] / details["shots"]
            if evaluation.feasible:
                feasible_counts += item["count"]
                feasible_utilities.append(evaluation.utility)
        assert feasible_counts / details["shots"] == details["feasible_sample_rate"]
        optimum = solve_exact(scenario, budget).evaluation.utility
        assert details["exact_optimum"] == optimum
        if result["status"] == "ok":
            assert result["utility"] == max(feasible_utilities)
            assert result["bitstring"] in {item["bitstring"] for item in details["distribution"]}
            assert details["optimality_gap"] == optimum - result["utility"]
        else:
            assert result["status"] == "no_feasible_sample" and not feasible_utilities
            assert result["bitstring"] is result["utility"] is result["metrics"] is None
            assert details["optimality_gap"] is None
        circuit = qasm2.loads(details["compiled_qasm2"])
        assert circuit.depth() == details["depth"]
        assert dict(circuit.count_ops()) == details["operation_counts"]
        logical = build_circuit(build_energy_table(scenario, budget),
                                details["parameters"]["gamma"] + details["parameters"]["beta"], details["p"])
        assert Statevector.from_instruction(circuit.remove_final_measurements(inplace=False)).equiv(
            Statevector.from_instruction(logical))
        assert len(details["optimizer_trace"]) == details["optimizer_evaluations"]
    print(f"PASS {path.name}: {len(runs)} solver records, quantum evidence and source hashes verified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()
    for filename in args.files:
        verify(filename)
