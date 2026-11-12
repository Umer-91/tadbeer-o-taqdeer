Project: TADBEER-O-TAQDEER (تدبیر و تقدیر) — Where Strategy Shapes Destiny.

# PHASE 3 — API INTEGRATION, VERIFICATION, REPORT & SUBMISSION
**Prerequisite:** Read MASTER_PLAN.md, Phase 1 and 2 progress logs. Preserve passing code. This is the release phase. Never conceal failures.

## Step 1 — Integrate FastAPI
Implement `backend/raasta/api.py` and request/response Pydantic models exactly matching MASTER_PLAN contract. GET `/api/health`, GET `/api/scenarios`, POST `/api/optimize`. Call the SAME evaluator and solvers used in Phase 1. For QAOA run, protect from too-long synchronous work with bounded iterations and clear timeout/error handling; show actual runtime. Validate scenario ID, budget (0..12 or documented range), shots, p, seed. Add CORS for local Next.js origins. Include `/docs` Swagger for technical judges. Add pytest TestClient tests for 200/422, correct objective, feasible results, QAOA counts and error states.

## Step 2 — Connect UI to reality
Replace preview fixtures with live API. On page load fetch scenarios; on run POST selected scenario, budget, algorithm, seed/shots. Render response.selected_actions on valley/network, update budget meter, service status, charts, evidence panel. Compare algorithms by making distinct real requests; no algorithm gets a cached result mislabeled as another. QAOA may be worse than exact; show gap honestly. On API error, display actionable failure with retry, never show sample numbers as if real. Include synthetic data badge everywhere appropriate. Ensure no mismatch in canonical bit order.

## Step 3 — End-to-end and experiment verification
Run complete setup from clean environment; test three scenarios and budgets 6,9,12 for exact and greedy; QAOA at least one meaningful case, more if runtime allows. Save actual experiment JSON/CSV with seed, shots, p, Python/Qiskit versions, CPU/environment, timestamps, objective, feasibility, gap, counts and runtime. Cross-check every reported bitstring with evaluator; exact exhaustive is ground truth. Include negative tests: bridge disabled, feeder disabled, budget 0, no feasible quantum sample, API offline, wrong inputs. Verify no screenshots/charts claim unmeasured improvements. Never cherry-pick seed as if representative; if multiple seeds, report all and aggregates.

## Step 4 — Architecture diagram
Create `docs/architecture.png` or SVG, embed in report. Nodes: Browser Next.js + R3F landing/dashboard -> FastAPI -> Scenario/Constraint Evaluator -> QAOA Qiskit simulator + Exact brute force + Greedy -> Typed JSON -> Visualizer/Charts. Indicate synthetic data and no real-world control. Avoid fake cloud services. Include a separate dependency diagram: access + power -> hospital, crossing + pump power -> water.

## Step 5 — Write professional Word report
Generate `docs/report.docx` with actual executed results and architecture diagram (not a PDF instead). Recommended 5–8 concise pages, clean typography, figures and tables:
1. Title, team info placeholders (do not invent names), domain Disaster Response.
2. Abstract and Pakistan motivation; fictional valley disclaimer.
3. Problem and stakeholders; 6 binary interventions, costs, budget, explicit dependency equations.
4. Mathematical objective and hard constraints; utility weights and their limitations; distinguish service score vs population.
5. Quantum mapping: state encoding, diagonal energy/penalty, circuit, p, mixer, optimizer, seeds/shots, limitations of exponential truth-table encoding.
6. Baselines exact 64-state enumeration and greedy marginal rule.
7. **Actual measured** results table and figure (only values from experiments/results), gaps and feasibility, environment versions; discuss poor quantum outcomes candidly.
8. Architecture figure, screenshot of real dashboard, original design rationale.
9. Limitations: synthetic data, simplified dependencies, no hydraulic/power-flow physics, small 6-qubit simulator, penalties, optimizer stochasticity, no speedup, no operational deployment.
10. Reproducibility instructions, references, asset credits, future work.
If results are missing, clearly say experiment failed or omit unsupported claims. Do not write fictitious numerical results.

## Step 6 — 3-minute pitch (strict timebox)
Create `docs/demo_script.md` with 180-second plan:
- 0:00–0:25 Pakistan flood/landslide story and three lifelines.
- 0:25–0:50 show dependency: bridge alone does not power hospital; feeder alone does not reconnect village.
- 0:50–1:20 formulate six choices, budget and score; why combinatorial.
- 1:20–2:15 live or pre-run **real** QAOA demo; show selected interventions and exact/greedy comparison. If live run too slow, use actual saved run clearly labeled recorded, not pretend live.
- 2:15–2:40 scenario switch and responsive before/after visual.
- 2:40–3:00 limitations, honest contribution, close.
Script includes exact onscreen actions, spoken words, backup plan for demo errors. User must record/upload video, make viewable by anyone with link, and verify length <=3 minutes.

## Step 7 — README and release
Top-level README: hero screenshot (only real captured screenshot), project overview, prerequisites, exact install commands for Python and Node, run backend/frontend in separate terminals, run tests, example curl API, reproducible experiment command, repository tree, limitations, data disclaimer, attribution, architecture diagram link. Include `.env.example` with local API base. `docs/submission_checklist.md`: GitHub public/readable link, README setup, .docx report with architecture diagram, 3-min video share link, actual form link `https://forms.gle/Xc7ticrDnBYoCvcv9`, link permission test, deadline Nov 12 23:59 PKT. Do not push after cutoff. Ask user approval before submitting form/publishing externally.

## Final QA gates
```
cd backend && python -m pytest -q
cd frontend && npm run build
# start backend and frontend; test API through UI
# run experiments; inspect output files; check docx opens
```
Verify package lock, no secrets, no broken links, no license violations, browser console clean, mobile works, reduced-motion works, error state works, actual Qiskit circuit run evidenced. Produce `docs/FINAL_STATUS.md` with PASS/FAIL per gate, exact command outputs, remaining issues, and deliverable paths. Never claim completion of the video, GitHub publishing, or submission form without evidence.

## Stop condition
Commit `release: integrated verified hackathon submission` only if tests pass, and only before deadline. If time is short, prioritize working QAOA, report and demo over ornamental 3D polish. Present a truthful readiness summary.

## Codex handoff prompt
'Implement PHASE_3_INTEGRATION.md following MASTER_PLAN.md and the existing Phase 1/2 code. Connect genuine quantum backend to the UI, test end-to-end, run and save real experiments, generate docx report with architecture diagram, and prepare a timed pitch and submission checklist. Do not invent results or submit/publish without approval. Run final gates and report pass/fail.'
