"""Exact six-qubit truth-table Hamiltonian; exponentially scaling construction."""

from dataclasses import dataclass

import numpy as np

from .evaluator import evaluate, violation_magnitude
from .schema import Scenario, validate_budget


def canonical_from_qiskit(bits: str) -> str:
    if not isinstance(bits, str) or len(bits) != 6 or set(bits) - {"0", "1"}:
        raise ValueError("expected a six-bit Qiskit measurement key")
    return bits[::-1]


@dataclass(frozen=True)
class EnergyTable:
    bitstrings: tuple[str, ...]
    energies: np.ndarray
    utilities: np.ndarray
    violations: np.ndarray
    penalty: float
    minimum_positive_violation: float
    scale: float


def build_energy_table(scenario: Scenario, budget: float | None = None) -> EnergyTable:
    budget = validate_budget(scenario.budget_default if budget is None else budget)
    # Statevector index i represents |q5..q0>; action xi belongs to qubit qi.
    bits = tuple(canonical_from_qiskit(f"{i:06b}") for i in range(64))
    utility = np.array([evaluate(x, scenario, budget).utility for x in bits], dtype=float)
    violations = np.array([violation_magnitude(x, scenario, budget) for x in bits])
    delta = float(np.min(violations[violations > 0]))
    # P * delta > utility spread, including fractional budget overflows.
    penalty = float((np.ptp(utility) + 1.0) / min(1.0, delta))
    energies = -utility + penalty * violations
    if not np.all(np.isfinite(energies)):
        raise ValueError("scenario energy range exceeds finite simulator precision")
    feasible = violations == 0
    # Guard the construction against numerical loss of the penalty guarantee.
    if np.min(energies[~feasible]) <= np.min(energies[feasible]):
        raise ValueError("energy penalty failed to separate feasible ground states")
    scale = max(1.0, float(np.max(np.abs(energies))))
    for array in (utility, violations, energies):
        array.setflags(write=False)
    return EnergyTable(bits, energies, utility, violations, penalty, delta, scale)
