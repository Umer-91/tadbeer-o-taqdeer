# Six-action restoration model

TADBEER-O-TAQDEER is a synthetic research prototype, not a deployed disaster response system. All places, village populations, priorities, and damage are fictional. Planning units are abstract, not PKR. Population/priority metadata does not enter the service utility and must not be presented as people saved.

## Variables and constraints

Action-order bitstrings are `x0..x5`:

| Index | ID | Cost |
|---|---|---:|
| 0 | bridge_repair | 4 |
| 1 | temporary_crossing | 2 |
| 2 | hospital_road | 2 |
| 3 | feeder_repair | 4 |
| 4 | hospital_solar | 3 |
| 5 | pump_generator | 2 |

Exactly six binary variables, enabled actions only, total scenario-specific cost <= supplied budget, and `x0+x1 <= 1`. Default budget is 9. Costs are positive integer planning units; budgets may be finite nonnegative real numbers. Modified scenario costs are honored. Invalid bitstrings receive infeasible evaluations with null scores; invalid budgets raise a validation error.

- `crossing = x0 OR x1`; `basic_connectivity = crossing`.
- `access = crossing AND x2`.
- `hospital_power = x3 OR x4`.
- `hospital_operational = access AND hospital_power`.
- `pump_power = x3 OR x5`.
- `water_operational = crossing AND pump_power`.

Feeder repair does not require road access. Dependencies are stylized service logic, not electrical/hydraulic simulations. Available interventions (`enabled`) are distinct from damaged links (`currently_working=false`). Link action references are illustrative associations, not a replacement for evaluator service logic.

`U = 50*hospital_operational + 30*water_operational + 15*basic_connectivity + 5*hospital_power - 0.5*cost`.

The utility is an abstract weighted service score. Coefficients are fixed by the original master plan, not selected to favor QAOA. The scenarios are `flood_baseline` (all enabled), `bridge_blocked` (x0 disabled), and `grid_extended_outage` (x3 disabled).

## Classical reference and greedy

Exact enumerates all 64 bitstrings, discards infeasible states, maximizes utility, then minimizes cost, then chooses the lexicographically smallest canonical bitstring. The all-zero vector is feasible for every accepted budget.

Greedy starts empty and adds the enabled feasible action with the largest strictly positive marginal utility per additional cost. Ties use lowest canonical action index. It stops when no positive addition remains. It never looks at the exact answer. Complementary actions can have negative marginal utility until their partners exist, so this deliberately myopic baseline can miss useful portfolios.

## Hamiltonian and penalty proof

This implements the master plan's allowed **diagonal six-qubit Hamiltonian**, not a quadratic QUBO or an efficient large-instance reduction. It builds all 64 energies explicitly:

`v(x) = max(0, cost-budget) + max(0, x0+x1-1) + sum(disabled selected actions)`.

Let `R = max_x U(x) - min_x U(x)` and `delta = min{v(x): v(x)>0}` over all 64 states. Choose `P = (R+1)/min(1,delta)` and `E(x) = -U(x)+P*v(x)`.

For any infeasible x and feasible y, `E(x)-E(y) = U(y)-U(x)+P*v(x) >= -R + P*delta >= 1 > 0`. Every global energy minimum is therefore feasible; among feasible states minimizing E is exactly maximizing U. Enumeration tests compare the complete set of energy minima to all utility-optimal feasible states. The secondary solver tie-break chooses a representative; it does not alter the Hamiltonian minima. `delta` handles fractional budgets where simply choosing `P>R` would not suffice for a fractional overflow. Energy arrays are indexed in Qiskit basis order.

## Genuine QAOA execution

Qubit qi encodes action xi. Qiskit displays measurement keys as q5..q0; reverse exactly six bits to obtain the canonical x0..x5 string. Tests prepare and measure all 64 computational basis states.

Prepare H on all six qubits. Each of p layers applies the actual Qiskit `DiagonalGate(exp(-i*gamma*E/S))` followed by `RX(2*beta)` on every qubit; `S=max(1,max(abs(E)))` is a positive normalization recorded in diagnostics. Rescaling preserves all energy minima and is explicitly reflected in the phase angles and optimizer objective. Default p=1; p=2 is supported.

SciPy COBYLA optimizes the exact expectation from `Qiskit Statevector.from_instruction`. These objective evaluations are classically simulated quantum circuits, not shot-based training. One seeded initial parameter vector is used; maxiter defaults to 60, and nonconvergence is disclosed. The final circuit is transpiled to standard `u3,cx` gates, measured, and executed with `AerSimulator(method='statevector')` using an explicit simulator seed and actual requested shots. This basis allows strict OpenQASM 2 replay without custom gate declarations; replay is tested for statevector equivalence. No sampling is substituted with a classical search or exact solver output.

Select the best feasible **observed** bitstring using the same deterministic rank rule. If none is measured, return `no_feasible_sample`, null scores/metrics, and an empty action list. Compute the exact reference only to report the absolute gap: `exact U - best feasible observed U`. A null gap means no feasible sample, not zero gap.

Record raw counts, canonical distribution, shots, p, seeds, initial/final parameters, every objective evaluation, optimizer convergence, feasible sample rate, gap, total runtime, transpiled depth/gate counts, compiled OpenQASM, logical circuit text, energy table/scale/penalty, source hashes, timestamp, and package versions. Gate count excludes measurement and barriers; depth is Qiskit's transpiled circuit depth including measurement. Runtime includes energy construction, optimization, sampling, exact comparison, and circuit evidence serialization, but excludes module import, package installation, and writing the result file.

## Scope and limitations

This six-qubit statevector/Aer demonstration runs on a classical simulator, with no noise model or hardware run. Hamiltonian construction is exponential and already enumerates the same state space as the exact baseline. It cannot support a quantum speedup claim. A best sample reaching the optimum does not mean the distribution is concentrated there or that QAOA outperforms exact/greedy in runtime. One seed is not a statistical performance study; all requested scenario/budget cases must be retained, including weak outcomes and optimizer failures.

See PROGRESS.md for actual measured outcomes and recorded JSON. All nine seed-42 runs sampled an exact-optimal feasible state, while feasible sample rates varied and every optimizer stopped at the evaluation cap without convergence. These best-sample outcomes are not distribution-wide optimality guarantees.

## API references consulted

- [IBM Qiskit DiagonalGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.DiagonalGate)
- [Qiskit AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)
