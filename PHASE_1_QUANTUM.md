Project: TADBEER-O-TAQDEER (تدبیر و تقدیر) — Where Strategy Shapes Destiny.

# PHASE 1 — QUANTUM SCIENCE & OPTIMIZATION ENGINE
**Prerequisite:** Read MASTER_PLAN.md completely. Implement backend core only. Do not create frontend, report or API in this phase.

## Goal
Produce a small, rigorous, reproducible optimization experiment that proves the quantum component actually does computational work. Do not optimize the aesthetics here. Commit only when evaluator, baselines and real Qiskit experiment are tested.

## Step-by-step tasks
1. Create Python project in `backend/` with tested/pinned dependencies, `.gitignore`, `backend/README.md`, tests and `docs/MODEL.md`. Determine installed Qiskit API version by running introspection and tiny smoke test, not assumptions.
2. Implement canonical `Action`, `Scenario`, `Evaluation`, `SolverResult` typed structures in `schema.py`. Exactly six actions, stable IDs: `bridge_repair`, `temporary_crossing`, `hospital_road`, `feeder_repair`, `hospital_solar`, `pump_generator`. Stable index x0..x5 and costs [4,2,2,4,3,2]. Use abstract budget units.
3. Implement `scenarios.py`: `flood_baseline` budget 9, all enabled; `bridge_blocked` x0 disabled; `grid_extended_outage` x3 disabled. Synthetic narrative, stylized nodes/links, no fake geocoordinates. Distinguish *action enabled* from *infrastructure currently working*. No geographic assertions.
4. Implement pure `evaluate(bitstring, scenario, budget)` in `evaluator.py`, exactly as master: feasibility, violation list, cost, access, hospital_power, hospital_operational, pump_power, water_operational, basic_connectivity, utility. Canonical string order x0..x5. Avoid rounding inconsistencies.
5. Implement exact solver: iterate `itertools.product((0,1), repeat=6)`; discard infeasible; maximize utility with cost/lexicographic tie-break. Return full diagnostics and 64 states evaluated. Unit test hand-computed cases: all zeros; only bridge; crossing+road+solar; crossing+feeder+generator; both bridge/crossing invalid; over-budget; disabled action.
6. Implement greedy solver with positive marginal utility / cost. Be explicit that complementarity makes greedy weak; record decision trace. If all single-action marginal gains zero, greedy may stop early — this is informative. Never use exact output to steer greedy.
7. Implement energy mapping. Recommended robust small-n approach: for every 6-bit state compute `E=-U+P*penalty` where penalty includes budget overflow, alternative exclusivity, disabled actions. Choose P via conservative bound based on U range (e.g. > max U - min U + margin). Verify all 64 energy values and that minimum-energy states correspond exactly to evaluator-optimal feasible states. Explain exponential truth-table construction and why it is not scalable.
8. Implement **real QAOA** with six qubits: prepare |+>^6, phase separator using actual Qiskit diagonal phase operation with energies, RX mixer, p=1 (p=2 optional), classical parameter optimization (e.g. COBYLA) over expectation value. Use simulator statevector expectation for parameter optimization and **actual measurement shots** for final distribution, or fully shot-based objective; disclose which. Correctly map Qiskit little-endian measurement strings to canonical x0..x5. Run at least one seeded experiment, save distribution, depth/gates, runtime, optimizer iterations and feasible sample rate. If API fails, fix environment; do not fake QAOA with enumeration/random sampling.
9. Select best **feasible observed** quantum bitstring; if none observed, return explicit `no_feasible_sample`. Compute gap to exact from authoritative evaluator. Don't present the exact solution as QAOA's result. Store real JSON under `experiments/results/` with seed, shots, p, package versions.
10. Implement tests: 64-state evaluator enumeration, deterministic tie-breaking, scenario constraints, QUBO/energy equivalence, endianness via known basis state, circuit has six qubits and nontrivial phase/mixer gates, counts sum to shots, decoded bitstrings length six, feasibility of reported solution. Keep quantum smoke tests fast with low shots/iterations; mark slow benchmarks separately.

## Acceptance commands (adjust and record actual commands)
```
cd backend
python -m pip install -e '.[dev]'
python -m pytest -q
python -m raasta.quantum --scenario flood_baseline --budget 9 --shots 512 --seed 42
```
All commands must be real and working, not aspirational. `docs/MODEL.md` must state exact U, constraints, scenario rules, energy penalty, QAOA circuit construction, caveats. Create `docs/PROGRESS.md` with exact test count, commands, observed outcome, known limitations. Git commit `feat: verified lifeline optimization core`.

## Don't do
No frontend. No network API. No external flood data. No fabricated figures. No claims of advantage. No change to six-action canonical contract without updating master and tests and explaining why. If computationally heavy, cap optimizer iterations and document that approximation may be poor. A weak but genuine QAOA result is acceptable; a fake perfect one is not.

## Codex handoff prompt
'Implement PHASE_1_QUANTUM.md using MASTER_PLAN.md as source of truth. Work only in backend core, tests, experiments and MODEL.md. Run and report commands and actual results. Stop at the Phase 1 gate; do not proceed to Phase 2 until asked.'
