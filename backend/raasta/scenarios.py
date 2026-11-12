"""Fictional fixtures, not observations of actual Pakistani communities."""

from dataclasses import replace

from .schema import ACTION_IDS, Action, Link, Node, Scenario

_LABELS = (
    "Repair main bridge", "Establish temporary crossing", "Repair hospital access road",
    "Repair electricity feeder", "Install hospital solar-battery backup", "Deploy pump generator",
)
_COSTS = (4, 2, 2, 4, 3, 2)
_ACTIONS = tuple(Action(aid, i, _LABELS[i], _COSTS[i]) for i, aid in enumerate(ACTION_IDS))
# Populations and weights are fictional descriptive metadata, NOT utility inputs.
_NODES = (
    Node("entry", "Valley entry", "gateway"),
    Node("village_a", "Fictional Village A", "village", 400, 1.0),
    Node("village_b", "Fictional Village B", "village", 250, 1.2),
    Node("village_c", "Fictional Village C", "village", 350, 1.1),
    Node("hospital", "Fictional valley hospital", "hospital"),
    Node("feeder", "Damaged feeder", "power"),
    Node("pump", "Fictional water pump", "water"),
)
_LINKS = (
    Link("crossing", "entry", "village_a", "road", ACTION_IDS[:2]),
    Link("hospital_route", "village_a", "hospital", "road", (ACTION_IDS[2],)),
    Link("feeder_hospital", "feeder", "hospital", "electricity", (ACTION_IDS[3],)),
    Link("feeder_pump", "feeder", "pump", "electricity", (ACTION_IDS[3],)),
    Link("water_b", "pump", "village_b", "water", (ACTION_IDS[3], ACTION_IDS[5])),
    Link("water_c", "pump", "village_c", "water", (ACTION_IDS[3], ACTION_IDS[5])),
)


def list_scenarios() -> tuple[Scenario, ...]:
    common = dict(budget_default=9, nodes=_NODES, links=_LINKS)
    return (
        Scenario("flood_baseline", "Synthetic valley flood",
                 "Fictional flood/landslide damage; all six interventions are available.",
                 actions=_ACTIONS, **common),
        Scenario("bridge_blocked", "Synthetic bridge unavailable",
                 "Fictional bridge repair cannot be undertaken; temporary crossing remains available.",
                 actions=tuple(replace(a, enabled=False) if a.index == 0 else a for a in _ACTIONS), **common),
        Scenario("grid_extended_outage", "Synthetic extended grid outage",
                 "Fictional feeder repair is unavailable; local power alternatives remain available.",
                 actions=tuple(replace(a, enabled=False) if a.index == 3 else a for a in _ACTIONS), **common),
    )


def get_scenario(scenario_id: str) -> Scenario:
    for scenario in list_scenarios():
        if scenario.id == scenario_id:
            return scenario
    raise ValueError(f"unknown scenario: {scenario_id!r}")
