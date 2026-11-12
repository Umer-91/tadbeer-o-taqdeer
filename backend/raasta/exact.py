"""Exhaustive 64-state classical ground truth."""

from time import perf_counter

from .evaluator import all_bitstrings, evaluate
from .schema import Scenario, SolverResult, selection_key, validate_budget


def solve_exact(scenario: Scenario, budget: float | None = None) -> SolverResult:
    start = perf_counter()
    budget = validate_budget(scenario.budget_default if budget is None else budget)
    evaluations = [evaluate(bits, scenario, budget) for bits in all_bitstrings()]
    feasible = [value for value in evaluations if value.feasible]
    best = min(feasible, key=selection_key)
    return SolverResult(scenario.id, "exact", budget, "ok", best, {
        "runtime_ms": (perf_counter() - start) * 1000,
        "states_evaluated": len(evaluations), "feasible_states": len(feasible),
        "optimal_bitstrings": [e.bitstring for e in feasible if e.utility == best.utility],
        "tie_break": "maximum utility, minimum cost, lexicographic x0..x5",
    })
