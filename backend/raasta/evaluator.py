"""Authoritative feasibility and utility, in action order x0..x5."""

from itertools import product

from .schema import Evaluation, Scenario, validate_budget


def all_bitstrings() -> tuple[str, ...]:
    return tuple("".join(map(str, bits)) for bits in product((0, 1), repeat=6))


def evaluate(bitstring: str, scenario: Scenario, budget: float | None = None) -> Evaluation:
    budget = validate_budget(scenario.budget_default if budget is None else budget)
    if not isinstance(bitstring, str) or len(bitstring) != 6 or set(bitstring) - {"0", "1"}:
        return Evaluation(None, (), None, False, ("invalid_binary_bitstring",), None,
                          None, None, None, None, None, None)
    x = tuple(int(bit) for bit in bitstring)
    cost = sum(action.cost * x[action.index] for action in scenario.actions)
    violations = []
    if cost > budget:
        violations.append("budget_exceeded")
    if x[0] + x[1] > 1:
        violations.append("exclusive_crossings")
    violations.extend(f"disabled_action:{a.id}" for a in scenario.actions if x[a.index] and not a.enabled)
    crossing = bool(x[0] or x[1])
    access = crossing and bool(x[2])
    power = bool(x[3] or x[4])
    hospital = access and power
    pump = bool(x[3] or x[5])
    water = crossing and pump
    utility = 50 * hospital + 30 * water + 15 * crossing + 5 * power - 0.5 * cost
    return Evaluation(bitstring, tuple(a.id for a in scenario.actions if x[a.index]),
                      cost, not violations, tuple(violations), utility,
                      access, power, hospital, pump, water, crossing)


def violation_magnitude(bitstring: str, scenario: Scenario, budget: float) -> float:
    evaluation = evaluate(bitstring, scenario, budget)
    if evaluation.total_cost is None:
        raise ValueError("energy requires exactly six binary digits")
    return (max(0.0, evaluation.total_cost - budget)
            + max(0, int(bitstring[0]) + int(bitstring[1]) - 1)
            + sum(int(bitstring[a.index]) for a in scenario.actions if not a.enabled))
