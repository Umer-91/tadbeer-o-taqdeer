"""Immutable domain types; backend authority for the shared API contract."""

from dataclasses import asdict, dataclass, field
from math import isfinite
from numbers import Real
from typing import Any, Literal

ACTION_IDS = (
    "bridge_repair", "temporary_crossing", "hospital_road",
    "feeder_repair", "hospital_solar", "pump_generator",
)


def validate_budget(budget: float) -> float:
    if isinstance(budget, bool) or not isinstance(budget, Real):
        raise ValueError("budget must be a finite nonnegative number")
    if not isfinite(budget) or budget < 0:
        raise ValueError("budget must be a finite nonnegative number")
    return float(budget)


@dataclass(frozen=True)
class Action:
    id: str
    index: int
    label: str
    cost: int
    enabled: bool = True

    def __post_init__(self) -> None:
        if type(self.index) is not int or not 0 <= self.index < 6:
            raise ValueError("action index must be an integer in 0..5")
        if self.id != ACTION_IDS[self.index]:
            raise ValueError("action ID must match its canonical index")
        if type(self.cost) is not int or self.cost <= 0:
            raise ValueError("action cost must be a positive integer planning unit")
        if type(self.enabled) is not bool:
            raise ValueError("enabled must be boolean")


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    kind: str
    population: int | None = None
    priority_weight: float | None = None


@dataclass(frozen=True)
class Link:
    id: str
    source: str
    target: str
    lifeline: Literal["road", "electricity", "water"]
    action_ids: tuple[str, ...]
    currently_working: bool = False


@dataclass(frozen=True)
class Scenario:
    id: str
    name: str
    description: str
    budget_default: float
    actions: tuple[Action, ...]
    nodes: tuple[Node, ...] = ()
    links: tuple[Link, ...] = ()
    synthetic: bool = True

    def __post_init__(self) -> None:
        validate_budget(self.budget_default)
        if not isinstance(self.actions, tuple) or len(self.actions) != 6:
            raise ValueError("scenario requires an immutable tuple of exactly six actions")
        if tuple(a.index for a in self.actions) != tuple(range(6)):
            raise ValueError("actions must be ordered x0..x5")
        if self.synthetic is not True:
            raise ValueError("this prototype accepts only explicitly synthetic scenarios")
        node_ids = {node.id for node in self.nodes}
        if len(node_ids) != len(self.nodes):
            raise ValueError("node IDs must be unique")
        if len({link.id for link in self.links}) != len(self.links):
            raise ValueError("link IDs must be unique")
        for link in self.links:
            if link.source not in node_ids or link.target not in node_ids:
                raise ValueError("link endpoints must reference scenario nodes")
            if any(action_id not in ACTION_IDS for action_id in link.action_ids):
                raise ValueError("link action IDs must be canonical")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Evaluation:
    bitstring: str | None
    selected_actions: tuple[str, ...]
    total_cost: int | None
    feasible: bool
    violations: tuple[str, ...]
    utility: float | None
    access: bool | None
    hospital_power: bool | None
    hospital_operational: bool | None
    pump_power: bool | None
    water_operational: bool | None
    basic_connectivity: bool | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def selection_key(value: Evaluation) -> tuple[float, int, str]:
    """Minimize this key: highest utility, least cost, lexical action order."""
    if not value.feasible or value.utility is None or value.total_cost is None:
        raise ValueError("only feasible evaluations can be ranked")
    assert value.bitstring is not None
    return -value.utility, value.total_cost, value.bitstring


@dataclass(frozen=True)
class SolverResult:
    scenario_id: str
    algorithm: Literal["exact", "greedy", "qaoa"]
    budget: float
    status: Literal["ok", "no_feasible_sample"]
    evaluation: Evaluation | None
    diagnostics: dict[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        e = self.evaluation
        return {
            "scenario_id": self.scenario_id, "algorithm": self.algorithm,
            "budget": self.budget, "status": self.status,
            "selected_actions": list(e.selected_actions) if e else [],
            "bitstring": e.bitstring if e else None,
            "feasible": e.feasible if e else None,
            "utility": e.utility if e else None,
            "total_cost": e.total_cost if e else None,
            "metrics": {key: getattr(e, key) for key in (
                "hospital_operational", "water_operational",
                "basic_connectivity", "hospital_power",
            )} if e else None,
            "diagnostics": self.diagnostics, "warnings": list(self.warnings),
        }
