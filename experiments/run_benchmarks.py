"""Measure all three synthetic scenarios at budgets 6/9/12 with one declared seed."""

import argparse
import json
from pathlib import Path

from raasta.exact import solve_exact
from raasta.greedy import solve_greedy
from raasta.provenance import environment_metadata
from raasta.scenarios import list_scenarios


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--shots", type=int, default=512)
    parser.add_argument("--maxiter", type=int, default=60)
    parser.add_argument("--classical-only", action="store_true", help="Explicitly run only classical baselines; no QAOA claims")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; measured records are never silently overwritten")
    runs = []
    for scenario in list_scenarios():
        for budget in (6, 9, 12):
            exact = solve_exact(scenario, budget)
            greedy = solve_greedy(scenario, budget)
            quantum = None
            if not args.classical_only:
                from raasta.quantum import solve_qaoa
                quantum = solve_qaoa(scenario, budget, seed=args.seed, shots=args.shots, maxiter=args.maxiter)
            run = {"scenario": scenario.to_dict(), "budget": budget,
                   "exact": exact.to_dict(), "greedy": greedy.to_dict()}
            if quantum is not None:
                run["qaoa"] = quantum.to_dict()
            runs.append(run)
            print(json.dumps({"scenario": scenario.id, "budget": budget, "exact": exact.evaluation.utility,
                              "greedy": greedy.evaluation.utility,
                              "qaoa": quantum.to_dict()["utility"] if quantum else "not run",
                              "feasible_sample_rate": quantum.diagnostics["feasible_sample_rate"] if quantum else None}), flush=True)
    payload = {"environment": environment_metadata(), "seed_policy": "seed 42 by default, fixed before runs; all nine cases retained",
               "seed": args.seed, "shots": args.shots, "maxiter": args.maxiter,
               "classical_only": args.classical_only, "runs": runs}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
