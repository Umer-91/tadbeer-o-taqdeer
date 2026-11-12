"""Myopic positive marginal utility per cost; no exact-solver guidance."""

from time import perf_counter

from .evaluator import evaluate
from .schema import Scenario, SolverResult, validate_budget


def solve_greedy(scenario: Scenario, budget: float | None = None) -> SolverResult:
    start = perf_counter()
    budget = validate_budget(scenario.budget_default if budget is None else budget)
    current = evaluate("000000", scenario, budget)
    trace = []
    while True:
        candidates = []
        for action in scenario.actions:
            if not action.enabled or current.bitstring[action.index] == "1":
                continue
            bits = list(current.bitstring)
            bits[action.index] = "1"
            candidate = evaluate("".join(bits), scenario, budget)
            gain = candidate.utility - current.utility
            if candidate.feasible and gain > 0:
                candidates.append((gain / action.cost, action.index, gain, candidate))
        if not candidates:
            break
        ratio, index, gain, current = min(candidates, key=lambda c: (-c[0], c[1]))
        trace.append({"action_id": scenario.actions[index].id, "marginal_utility": gain,
                      "gain_per_cost": ratio, "bitstring": current.bitstring,
                      "utility": current.utility, "total_cost": current.total_cost})
    return SolverResult(scenario.id, "greedy", budget, "ok", current,
                        {"runtime_ms": (perf_counter() - start) * 1000, "decision_trace": trace,
                         "tie_break": "highest positive gain/cost, then lowest action index",
                         "stop_reason": "no feasible positive marginal addition"},
                        ("Myopic greedy can miss service complementarities; not a bound on optimal utility.",))
