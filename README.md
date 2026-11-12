# TADBEER-O-TAQDEER (تدبیر و تقدیر)

**Where Strategy Shapes Destiny.**

Quantum-assisted disaster recovery optimization for roads, electricity, and water in Pakistan. Formerly RAASTA-Q.

This is a reproducible research prototype using a fictional, Pakistan-inspired valley and explicitly synthetic data. It is not an operational disaster-management system and makes no claim of quantum advantage.

## Current status

Repository setup and documentation scaffold only. The quantum engine, API, frontend, application tests, and benchmarks have **not** been implemented or run. Do not interpret empty directories as working components. See [progress](docs/PROGRESS.md) and [decisions](docs/DECISIONS.md).

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

An authorized GitHub account is required while the repository is private. Authenticate through your Git credential manager's browser flow; never paste credentials into files or remote URLs.

```sh
git clone https://github.com/Umer-91/tadbeer-o-taqdeer.git
cd tadbeer-o-taqdeer
git switch main
git status
git rev-parse HEAD
git ls-remote origin refs/heads/main
git diff --check
```

Compare the local HEAD with the remote main hash. No package installation is required for this documentation scaffold. Python 3.11+ is planned; Python/Qiskit and Node/frontend dependencies will be selected, tested, pinned, and locked during their implementation phases. Application installation and execution commands are intentionally deferred until they can be verified.

## Development workflow

`main` is the stable integration branch. Develop sequentially on `phase-1-quantum`, `phase-2-frontend`, and `phase-3-integration`; start each phase from the latest integrated main. Review [CONTRIBUTING.md](CONTRIBUTING.md) before committing. No phase starts automatically after setup.

Commit tested work with meaningful messages, update `docs/PROGRESS.md`, push without force, and verify the remote hash. Keep secrets, virtual environments, and generated dependency directories out of Git. Keep lockfiles and measured experiment outputs in Git.

**Deadline:** November 12, 2026 at 23:59 Pakistan time (18:59 UTC). No commits or pushes at or after the cutoff. Making the repository public and submitting the project require explicit user approval.
