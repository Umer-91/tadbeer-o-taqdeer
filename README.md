# TADBEER-O-TAQDEER (تدبیر و تقدیر)

**Where Strategy Shapes Destiny.**

Quantum-assisted disaster recovery optimization for roads, electricity, and water in Pakistan. Formerly RAASTA-Q.

This is a reproducible research prototype using a fictional, Pakistan-inspired valley and explicitly synthetic data. It is not an operational disaster-management system and makes no claim of quantum advantage.

## Current status

Phase 1 core is verified on `phase-1-quantum`: **86 tests pass**, including real Qiskit/Aer execution, all-state energy equivalence, bit ordering, seeded reproducibility, and circuit export replay. The acceptance run and all nine synthetic scenario/budget experiments are recorded. Phase 2 adds the Urdu cinematic 3D frontend and typed dashboard on `phase-2-frontend`: **11 client tests pass**, with lint/typecheck/build and responsive browser checks. The HTTP API and end-to-end integration remain Phase 3 work. See [progress and push status](docs/PROGRESS.md), [frontend setup](frontend/README.md), [visual QA](docs/FRONTEND_QA.md), and [backend setup](backend/README.md).

Default flood/budget 9, seed 42, p=1, 512 shots: QAOA sampled `011100` with utility 96 and 87.5% feasible shots. This best observed score matches exact; the optimizer hit its 60-evaluation cap without convergence. These are small noiseless simulator results, not evidence of quantum advantage.

## Source specifications

Read [MASTER_PLAN.md](MASTER_PLAN.md) before changing architecture. The complete original technical requirements are retained with branding updates:

1. [Phase 1: quantum science and optimization](PHASE_1_QUANTUM.md)
2. [Phase 2: cinematic website](PHASE_2_CINEMATIC_WEB.md)
3. [Phase 3: integration and verification](PHASE_3_INTEGRATION.md)

The model remains six binary interventions, exact enumeration of all 64 states, the specified service utility and constraints, and genuine Qiskit QAOA execution. The future backend is authoritative for scenarios, feasibility, and scores. No frontend solver outputs may be fabricated.

## Repository layout

```text
backend/raasta/         Python optimization engine and later FastAPI API
backend/tests/          Evaluator, solver, circuit and API tests
frontend/src/app/      Next.js App Router
frontend/src/components/{landing,dashboard,shared}/
frontend/src/lib/      Typed API client and TypeScript contracts
frontend/public/       Static assets
shared/scenarios/      Future exported synthetic scenario fixtures
shared/contracts/      Future generated API schemas
tests/{integration,e2e}/
experiments/results/   Actual measured outputs only
docs/assets/           Architecture and report assets
```

`backend/raasta` retains the original internal package identifier for technical consistency. Product branding is Tadbeer-o-Taqdeer. See [architecture](docs/ARCHITECTURE.md).

## Clone and inspect

The repository is public with user approval. Reading/cloning needs no account; pushes require authorized GitHub access. Authenticate through your Git credential manager's browser flow; never paste credentials into files or remote URLs.

```sh
git clone https://github.com/Umer-91/tadbeer-o-taqdeer.git
cd tadbeer-o-taqdeer
git switch main
git status
git rev-parse HEAD
git ls-remote origin refs/heads/main
git diff --check
```

Compare the local HEAD with the corresponding remote branch hash. For the frontend and core together, switch to `phase-2-frontend` and follow [frontend setup](frontend/README.md). The pinned numerical stack requires Python 3.12+; quantum validation used the user's Python 3.12.10 and a repository-root virtual environment. Frontend validation used Node 24.22.1 and the committed npm lockfile.

## Development workflow

`main` is the stable integration branch. Develop sequentially on `phase-1-quantum`, `phase-2-frontend`, and `phase-3-integration`; start each phase from the latest integrated main. Review [CONTRIBUTING.md](CONTRIBUTING.md) before committing. No phase starts automatically after setup.

Commit tested work with meaningful messages, update `docs/PROGRESS.md`, push without force, and verify the remote hash. Keep secrets, virtual environments, and generated dependency directories out of Git. Keep lockfiles and measured experiment outputs in Git.

**Deadline:** November 12, 2026 at 23:59 Pakistan time (18:59 UTC). No commits or pushes at or after the cutoff. Making the repository public and submitting the project require explicit user approval.

## Integrated local startup

On phase-3-release, follow backend/README.md to install the Python lockfile. In terminal one run `.venv/Scripts/python.exe -m uvicorn raasta.api:app --host 127.0.0.1 --port 8000`. In terminal two use `cd frontend`, `npm ci`, `npm run build`, then `npm run start`. Open http://127.0.0.1:3000; Swagger is at http://127.0.0.1:8000/docs. Phase 3 verification status and outstanding gates are in docs/FINAL_STATUS.md. The Word report exists but is not yet visually verified. No submission has been performed.
