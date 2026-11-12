from dataclasses import replace

import numpy as np
import pytest

from raasta.energy import build_energy_table
from raasta.evaluator import all_bitstrings, evaluate
from raasta.exact import solve_exact
from raasta.greedy import solve_greedy
from raasta.scenarios import get_scenario, list_scenarios
from raasta.schema import selection_key


@pytest.mark.parametrize("bits,cost,utility,hospital,water,power", [
    ("000000", 0, 0, False, False, False),
    ("100000", 4, 13, False, False, False),
    ("011010", 7, 66.5, True, False, True),
    ("010101", 8, 46, False, True, True),
    ("011100", 8, 96, True, True, True),
    ("000100", 4, 3, False, False, True),
])
def test_hand_computed_services(bits, cost, utility, hospital, water, power):
    result = evaluate(bits, get_scenario("flood_baseline"))
    assert result.feasible
    assert (result.total_cost, result.utility) == (cost, utility)
    assert result.hospital_operational is hospital
    assert result.water_operational is water
    assert result.hospital_power is power


@pytest.mark.parametrize("scenario", list_scenarios(), ids=lambda s: s.id)
@pytest.mark.parametrize("budget", [0, 6, 9, 12])
def test_every_state_against_independent_set_model(scenario, budget):
    """Independent set-based oracle covers all 64 choices, not solver outputs."""
    for bits in all_bitstrings():
        selected = {i for i, value in enumerate(bits) if value == "1"}
        cost = sum(scenario.actions[i].cost for i in selected)
        connected = bool(selected & {0, 1})
        powered = bool(selected & {3, 4})
        hospital = connected and 2 in selected and powered
        water = connected and bool(selected & {3, 5})
        feasible = (cost <= budget and not {0, 1} <= selected
                    and all(scenario.actions[i].enabled for i in selected))
        result = evaluate(bits, scenario, budget)
        assert result.feasible == feasible
        assert result.utility == 50 * hospital + 30 * water + 15 * connected + 5 * powered - cost / 2
        assert result.total_cost == cost
        assert result.access == (connected and 2 in selected)
        assert result.pump_power == bool(selected & {3, 5})
        assert bool(result.violations) != feasible
        assert result.selected_actions == tuple(scenario.actions[i].id for i in sorted(selected))


@pytest.mark.parametrize("bits,scenario,budget,violation", [
    ("110000", "flood_baseline", 9, "exclusive_crossings"),
    ("111111", "flood_baseline", 9, "budget_exceeded"),
    ("100000", "bridge_blocked", 9, "disabled_action:bridge_repair"),
    ("000100", "grid_extended_outage", 9, "disabled_action:feeder_repair"),
])
def test_hard_constraints(bits, scenario, budget, violation):
    result = evaluate(bits, get_scenario(scenario), budget)
    assert not result.feasible
    assert violation in result.violations


@pytest.mark.parametrize("bits", ["", "0", "0000000", "10000x", " 00000", 101000, None, [0]*6])
def test_invalid_bitstrings_are_not_scored(bits):
    result = evaluate(bits, get_scenario("flood_baseline"))
    assert result.violations == ("invalid_binary_bitstring",)
    assert not result.feasible and result.utility is None and result.total_cost is None


@pytest.mark.parametrize("budget", [-1, float("nan"), float("inf"), "9", True])
def test_invalid_budgets(budget):
    scenario = get_scenario("flood_baseline")
    for solver in (solve_exact, solve_greedy, build_energy_table):
        with pytest.raises(ValueError):
            solver(scenario, budget)


@pytest.mark.parametrize("scenario", list_scenarios(), ids=lambda s: s.id)
@pytest.mark.parametrize("budget", [0, 6, 9, 12, 5.9, np.nextafter(6.0, 0.0)])
def test_energy_ground_states_equal_all_feasible_optima(scenario, budget):
    table = build_energy_table(scenario, budget)
    exact = solve_exact(scenario, budget)
    assert len(table.energies) == len(set(table.bitstrings)) == 64
    assert table.penalty * table.minimum_positive_violation > np.ptp(table.utilities)
    minima = {table.bitstrings[i] for i in np.flatnonzero(table.energies == min(table.energies))}
    assert minima == set(exact.diagnostics["optimal_bitstrings"])
    for i, bits in enumerate(table.bitstrings):
        result = evaluate(bits, scenario, budget)
        assert table.energies[i] == -result.utility + table.penalty * table.violations[i]
        assert (table.violations[i] == 0) == result.feasible
    assert exact.evaluation.feasible


@pytest.mark.parametrize("scenario", list_scenarios(), ids=lambda s: s.id)
@pytest.mark.parametrize("budget", [0, 6, 9, 12])
def test_baselines_and_greedy_trace(scenario, budget):
    exact, greedy = solve_exact(scenario, budget), solve_greedy(scenario, budget)
    assert exact.diagnostics["states_evaluated"] == 64
    assert exact.evaluation.utility >= greedy.evaluation.utility
    assert exact.evaluation == solve_exact(scenario, budget).evaluation
    assert greedy.evaluation == solve_greedy(scenario, budget).evaluation
    previous = evaluate("000000", scenario, budget)
    for step in greedy.diagnostics["decision_trace"]:
        current = evaluate(step["bitstring"], scenario, budget)
        assert current.feasible and current.utility > previous.utility
        assert sum(a != b for a, b in zip(previous.bitstring, current.bitstring)) == 1
        previous = current
    assert previous == greedy.evaluation
    assert greedy.evaluation.feasible
    if budget == 0:
        assert exact.evaluation.bitstring == greedy.evaluation.bitstring == "000000"


def test_exact_known_optimum_and_greedy_complementarity():
    scenario = get_scenario("flood_baseline")
    assert solve_exact(scenario).evaluation.bitstring == "011100"
    assert solve_exact(scenario).evaluation.utility == 96
    assert solve_greedy(scenario).evaluation.utility == 95.5
    assert solve_exact(scenario, 6).evaluation.utility == 47
    assert solve_greedy(scenario, 6).evaluation.utility == 43


def test_cost_changes_are_used_and_lexical_tie_break():
    original = get_scenario("flood_baseline")
    scenario = replace(original, actions=tuple(replace(a, cost=2) if a.index == 0 else a for a in original.actions))
    exact = solve_exact(scenario, 8)
    assert set(exact.diagnostics["optimal_bitstrings"]) == {"101100", "011100"}
    assert exact.evaluation.bitstring == "011100"
    assert evaluate("100000", scenario).total_cost == 2
    table = build_energy_table(scenario, 8)
    assert {table.bitstrings[i] for i in np.flatnonzero(table.energies == min(table.energies))} == {"101100", "011100"}
    # Explicitly exercise the secondary cost key independently of the fixed utility.
    same_utility_more_cost = replace(exact.evaluation, total_cost=9)
    assert selection_key(exact.evaluation) < selection_key(same_utility_more_cost)


def test_scenario_contract_and_synthetic_metadata():
    scenario = get_scenario("flood_baseline")
    assert [a.cost for a in scenario.actions] == [4, 2, 2, 4, 3, 2]
    assert sum(n.kind == "village" for n in scenario.nodes) == 3
    assert all(not link.currently_working for link in scenario.links)
    assert all(a.enabled for a in scenario.actions)
    with pytest.raises(ValueError):
        get_scenario("real_flood")
    with pytest.raises(ValueError):
        replace(scenario, actions=scenario.actions[::-1])
    with pytest.raises(ValueError):
        replace(scenario.actions[0], cost=0)
    with pytest.raises(ValueError):
        replace(scenario.actions[0], id="fake")
    with pytest.raises(ValueError):
        replace(scenario, synthetic=False)
