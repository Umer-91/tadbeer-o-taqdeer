# TADBEER-O-TAQDEER — MASTER PLAN / SOURCE OF TRUTH
Version: 1.0 | Qiskit Fall Fest 2026 | Deadline: 12 Nov 2026, 23:59 PKT

> **Read this file before every phase.** This is a reproducible research prototype, NOT an operational disaster-management system. Prioritize verifiable Qiskit computation over animation. Use fictional/synthetic data clearly labeled as such. Never invent results, citations, performance, quantum advantage, or deployed capabilities.

## 0. Mission and success definition
TADBEER-O-TAQDEER (تدبیر و تقدیر) — Where Strategy Shapes Destiny. Formerly RAASTA-Q (Resilient Access and Adaptive Service Restoration through Quantum Optimization). Domain submitted: **Disaster Response** (energy and water are dependent lifelines, not separate submitted domains). Pakistan-inspired fictional flood/landslide valley. Optimize a **portfolio of restoration interventions** that jointly restore transport access, electricity and safe-water service under a constrained budget. Novelty argument: cross-lifeline dependency-aware service restoration and visual explanation, **not** a claim that nobody has studied interdependent infrastructure.

Judge must be able to: (1) see a clear problem, objective, variables and constraints; (2) reproduce an exact classical solution; (3) run an actual Qiskit quantum circuit or QAOA workflow on a simulator and inspect measurement counts; (4) compare candidate scores and feasibility; (5) understand limitations; (6) watch a compelling 3-minute demo. **No quantum speedup required or promised.**

## 1. Non-negotiable scope and priority
P0: deterministic scenario data, evaluator, exhaustive exact baseline, genuinely executing Qiskit quantum optimization, tests, FastAPI response, dashboard controls and truthful output, README, report, demo script. P1: polished 3D valley and scroll narrative, accessible responsive design, charts, before/after network, quantum circuit view. P2: advanced shaders, particles, atmospheric water, extra scenarios, sound. If behind schedule, remove P2 before P0; never fake backend data to preserve UI.

## 2. One-account execution protocol
One Codex project/repo. Execute phases sequentially; after each phase run tests and commit. Read MASTER_PLAN.md + active phase file only; summarize existing repository before modifying. Maintain `docs/DECISIONS.md` and `docs/PROGRESS.md` (done, tested, remaining, blockers, commands). Don't overwrite passing code without tests. If blocked by dependency/version mismatch, inspect installed APIs and adjust with tests; record actual versions. No broad refactors in final hour. If moving accounts, push branch, clone same repo, read these files and progress log; never assume conversation history transfers.

## 3. Repository layout and file ownership
```
tadbeer-o-taqdeer/
  MASTER_PLAN.md
  PHASE_1_QUANTUM.md
  PHASE_2_CINEMATIC_WEB.md
  PHASE_3_INTEGRATION.md
  README.md
  .gitignore
  backend/
    pyproject.toml (or requirements.txt with pinned tested versions)
    raasta/
      __init__.py
      schema.py            # canonical typed schema
      scenarios.py         # synthetic data
      evaluator.py         # authoritative feasibility/objective
      exact.py             # exhaustive solver
      greedy.py            # baseline
      quantum.py           # QUBO + actual Qiskit circuit/QAOA
      api.py               # FastAPI
    tests/
  frontend/
    package.json
    src/app/               # Next.js app router
    src/components/        # landing, terrain, dashboard, charts
    src/lib/api.ts
    src/lib/types.ts
  experiments/
    run_benchmarks.py
    results/                # measured JSON/CSV only
  docs/
    DECISIONS.md
    PROGRESS.md
    MODEL.md
    ARCHITECTURE.md
    architecture.png
    report.docx
    demo_script.md
    submission_checklist.md
```

## 4. Canonical scientific model (do not silently change)
Use **six binary action variables** for the first working instance, with no fake 7th variable. Indices and meanings:
- x0: repair main bridge, cost 4
- x1: establish temporary crossing, cost 2
- x2: repair hospital access road, cost 2
- x3: repair electricity feeder, cost 4
- x4: install hospital solar-battery backup, cost 3
- x5: deploy pump generator, cost 2
Default budget = 9 abstract **planning units**, not PKR; explicitly synthetic. Scenario may disable actions or modify costs, but the evaluator must use the scenario supplied. Three fictional villages, population/priority weights in scenarios.py. No real geography or claims about actual hospitals, bridges or disasters.

**Illustrative dependency logic (must be implemented consistently):**
- `access = (x0 OR x1) AND x2` (hospital route).
- `hospital_power = x3 OR x4`.
- `hospital_operational = access AND hospital_power`.
- `pump_power = x3 OR x5`.
- `water_operational = (x0 OR x1) AND pump_power` (repair/deployment crew access to pump; simplifying assumption).
- `basic_connectivity = x0 OR x1`.
- `x0` and `x1` represent alternatives; enforce `x0+x1 <= 1` to avoid redundant selection. Optional extra scenario constraints must be explicit.
- **No assumption that power feeder restoration needs road access** unless explicitly added to both evaluator and quantum formulation. All dependencies are stylized, not hydraulic/electrical power-flow simulation.

Canonical **utility** for demo, fixed and documented (choose coefficients deliberately, not retrofitted to favor QAOA):
```
U(x) = 50*hospital_operational + 30*water_operational
       + 15*basic_connectivity + 5*hospital_power
       - 0.5*total_cost
```
This is an abstract weighted **service score**, not literal people saved. Budget and action exclusivity are hard feasibility constraints. Display service indicators individually and costs. Do not call utility 'people restored'. A separate population-weighted metric may be shown only if precisely defined from synthetic village weights and not confused with U. The core demonstration can compare coupled U to a naive greedy baseline; do not claim superiority without actual measurements.

For a scenario `s`, feasibility = binary length 6, enabled actions, sum(cost_i*x_i) <= budget, x0+x1 <= 1. Evaluate ALL 64 bitstrings for exact baseline, with stable deterministic tie-breaking: maximize U; then minimize cost; then lexicographic bitstring. Include zero vector feasible. `selected_actions`, `total_cost`, `feasible`, `violations`, `utility`, `hospital_operational`, `water_operational`, `basic_connectivity`, `hospital_power` are authoritative computed fields.

## 5. Quantum formulation and scientific honesty
Need **genuine quantum computation**. QAOA-compatible Ising/QUBO formulation with an explicit exact correspondence to the evaluator, or use a feasible-state variational quantum approach if QUBO expansion becomes prohibitive; document any deviation. Use binary polynomial substitutions and auxiliary variables for OR/AND, plus penalties for budget and exclusivity; alternatively build a diagonal cost Hamiltonian directly from the evaluator truth table for 6 qubits, which **exactly** represents U and feasibility via penalties. A 6-qubit diagonal phase separator constructed from all 64 energies is acceptable as a meaningful small-instance QAOA demonstration, provided it is actually implemented as quantum gates and sampled, and clearly disclosed as exponentially scaling construction. Set `E(x) = -U(x) + P*violations(x)` with P chosen > maximum utility spread, and verify global argmin E matches exact feasible argmax U. For cost overflow use `max(0,cost-budget)` penalty; disabled actions and exclusivity penalized. Document penalty proof/bound and enumerate all states in tests.

QAOA p=1 default, optional p=2 if performance permits. Uniform |+> initial state, phase separator from E, mixer RX, classical optimizer (e.g. COBYLA), statevector or Aer shot-based measurement with explicit seed. Record shots, depth, gate counts, parameter values, optimizer evaluations, distribution, best feasible sampled bitstring, objective and optimality gap vs exact. **Do not call a classical random search 'QAOA'.** Use Qiskit APIs compatible with actually installed pinned versions; if `qiskit_algorithms`/Aer needed install and document. Real shot counts and actual outputs only. Bit ordering (Qiskit little endian) must be tested against action indices. A diagonal `DiagonalGate`/phase operation can be used if supported, but avoid exponential unscalable claims. Never imply runtime advantage from this tiny simulator experiment.

## 6. Baselines and experiments
Exact enumerates 64 choices. Greedy: start empty, repeatedly add one enabled feasible action with highest **positive marginal utility gain per additional cost**; ties stable; stop when no positive addition. This greedy is intentionally myopic and can miss complementarities. Document that weakness. Optionally include a simple standalone-infrastructure heuristic but not required. Run 3 synthetic scenarios (normal flood, bridge unavailable, feeder unavailable), 3 budgets (6, 9, 12) only after baseline is stable; use fixed seeds; save real outputs with environment versions and timestamps. QAOA metrics: feasible sample rate, best feasible objective, optimality gap, total runtime, shots. If QAOA returns no feasible sample, show that fact rather than substituting exact answer.

## 7. Canonical API contract
Backend owns authoritative scenario data and evaluation. Frontend must never compute a fake optimization result. Pydantic models or equivalent:
```
GET /api/health -> {status, version, qiskit_available}
GET /api/scenarios -> [{id, name, description, budget_default, actions:[{id,index,label,cost,enabled}], nodes, links, synthetic:true}]
POST /api/optimize
 request: {scenario_id:string, budget:number, algorithm:"exact"|"greedy"|"qaoa", seed?:number, shots?:number, p?:number}
 response: {scenario_id, algorithm, budget, status:"ok"|"no_feasible_sample"|"error", selected_actions:string[], bitstring:string|null, feasible:boolean|null, utility:number|null, total_cost:number|null, metrics:{hospital_operational:boolean,water_operational:boolean,basic_connectivity:boolean,hospital_power:boolean}|null, diagnostics:{runtime_ms:number, shots?:number, depth?:number, gate_count?:number, feasible_sample_rate?:number, distribution?:[{bitstring,probability,count}], optimizer_evaluations?:number, exact_optimum?:number, optimality_gap?:number}, warnings:string[]}
```
`bitstring` is **canonical action order x0..x5** (e.g. '101000'), NOT Qiskit's display endianness. Validate budget, shots, p and scenario; 422 on invalid input, explicit 503/500 on unavailable computation, no silent fallback. CORS allow localhost frontend via env; no open wildcard in production. API integration tests assert all selected actions are feasible and metrics agree with evaluator.

## 8. Visual design contract: cinematic but credible
Design language: deep obsidian (#06070B), restrained ultraviolet (#895CFF), ice cyan (#48D8F3), electricity amber (#FFBC61), water blue (#4A91FF), damage coral (#FF5F6D). Use generous spacing, editorial typography, soft volumetric light, tasteful bloom, subtle grid/noise, physically plausible motion. Avoid generic AI SaaS gradients, giant rounded cards everywhere, endless glowing boxes, emoji-heavy UI. Strong typography and whitespace. Make **landing cinematic**, **dashboard readable**. Road = cyan, power = amber, water = blue, damage = coral; colors consistent in legends and accessibility labels.

Landing narrative: (1) floating stylized mountainous valley (not actual GIS) with 3 lifelines; (2) scroll triggers disaster and network failures; (3) show why coupled restoration matters; (4) transition to dashboard. Mouse orbit/drag, scroll-controlled camera, pointer hover labels; 3D scene changes state, not a video. In dashboard: network view, scenario selector, budget slider, QAOA/exact/greedy buttons, selected action list, service impact, comparison chart, circuit/measurement evidence panel. Clearly distinguish **cinematic illustration** from **computed solution**. On clicking Run, call backend; show loading, success, error, no feasible result. Before/after highlights must use response.selected_actions; never animate random links as 'optimized'. Add `prefers-reduced-motion`, keyboard support, mobile simplified fallback, no heavy shaders on weak devices. No user data collection.

### Urdu identity requirement (user addition, 2026-11-12)
The authentic Urdu project name **تدبیر و تقدیر** is the main hero headline, large and visually striking, with **TADBEER-O-TAQDEER** underneath. Tagline: **Where Strategy Shapes Destiny.** Show the Urdu branding in the loading sequence, main hero, and footer; keep the rest of the website primarily in English for international judges.

Render Urdu as real, selectable website text, never an AI-generated image. Use a beautiful, properly rendered Urdu Nastaliq font with an appropriate fallback, correct right-to-left rendering, and connected letter shapes. Make the identity intentional, premium, culturally authentic, and integral to the website. Use subtle violet illumination and cinematic reveals, while honoring reduced-motion preferences. Verify readability, line height, clipping, fallback rendering, and layout on mobile. Do not animate individual letters in a way that breaks Urdu shaping.

## 9. Tech stack and environment
Frontend: Next.js App Router, React, TypeScript, Tailwind, shadcn/ui where useful, React Three Fiber + drei + Three.js, GSAP ScrollTrigger (verify plugin availability/license), Recharts, optional React Flow. Avoid MapLibre unless real geospatial tiles add value; the synthetic network is better as custom 3D/2D graph. Backend: Python 3.11+, FastAPI, Pydantic, Qiskit, Qiskit Aer and/or algorithms package as actually compatible. Use tested versions and lockfiles; record exact commands. Don't overinstall packages. Local demo first; deployment optional and must not block submission.

## 10. Engineering rules / anti-hallucination contract
- Do not invent measurements, experiments, package versions, source citations, real map coordinates, population figures or testimonials.
- Clearly label all synthetic data and scenario assumptions in UI, README and report.
- No fake 'quantum' animation as proof of computation; expose circuit and counts.
- No hardcoded solver results; a deterministic cinematic *preview* is allowed only if marked as illustrative.
- Fail visibly on missing backend; don't silently return mocked API responses in production.
- Do not write a report until actual experiment outputs exist. Placeholders must be labeled TODO.
- Use tests for each dependency and bit ordering; verify objective/penalty consistency over all 64 states.
- Check no secrets committed. Use `.env.example`, no API keys in frontend.
- Avoid plagiarism and credit external assets/code. Prefer procedural geometry over unlicensed assets.
- Do not commit after contest cutoff. Submission requires user approval; never submit automatically.

## 11. Judging alignment (100 points)
Problem validity 20: Pakistan context, motivation, precise feasible optimization. Quantum utilization 25: legitimate QAOA circuit and mapping, explain assumptions. Implementation & validation 25: reproducible code, verified results, exact baseline. Innovation 15: coupled lifeline dependencies and restoration alternatives, modest novelty claims. Presentation 15: coherent cinematic story, readable live dashboard, 3-minute demonstration, answers to likely questions.

## 12. Definition of done / gate checklist
- `python -m pytest` passes; evaluator/penalty equivalence and bit ordering tested.
- At least one actual QAOA run produces recorded counts, optimizer trace, and feasibility assessment; failures honestly documented.
- Exact and greedy baseline work for all 3 scenarios; no infeasible selected plans.
- Frontend builds and runs; landing 3D interactive, dashboard sends real API requests.
- UI states include loading, error, success, empty; mobile/reduced-motion fallback.
- `README.md` fresh-machine setup with exact Python/node commands and expected results.
- `docs/report.docx` includes motivation, model, architecture diagram, QAOA mapping, methods, real comparison, limitations, references/credits.
- `docs/demo_script.md` 3-minute timed pitch; actual recorded video and public Drive link are USER tasks unless access explicitly provided.
- GitHub link, .docx report, architecture diagram inside report, video link verified before submission; don't claim done until checked.

## 13. Order of operations
1. Phase 1: lock model, implement evaluator/exact/greedy/QAOA, run tests, commit.
2. Phase 2: create cinematic Next.js UI with typed API client; use clearly labeled fixture data ONLY for layout development; commit.
3. Phase 3: FastAPI endpoints, connect UI, run experiments, produce docx, integration tests, final demo; commit.
If insufficient time: ship a beautiful functional 2D network dashboard + genuine quantum proof before advanced 3D. Preserve P0 at all costs.
