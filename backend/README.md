# Tadbeer-o-Taqdeer optimization core

Python package: `raasta`. Canonical model: [MODEL.md](../docs/MODEL.md). The API is deferred to Phase 3. All scenarios are fictional and synthetic.

## Reproducible environment

Quantum validation ran on **Python 3.12.10** from the user's local installation. The pinned NumPy/SciPy releases require Python >=3.12 (within the master's Python 3.11+ requirement). Dependencies and all transitive versions are in `requirements.lock.txt`. No IBM account or hardware credentials are required. The repository-root `.venv` is the working environment; the earlier `backend/.venv` is retained but unused.

From the repository root, on Windows PowerShell (select your installed Python 3.12 with the launcher):

```powershell
py -0p
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install --index-url https://pypi.org/simple -r backend/requirements.lock.txt
.venv/Scripts/python.exe -m pip install --no-deps --no-build-isolation -e 'backend[dev]'
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe -m pytest -q backend/tests
.venv/Scripts/python.exe -m raasta.quantum --scenario flood_baseline --budget 9 --shots 512 --seed 42 --output experiments/results/qaoa-new-run.json
.venv/Scripts/python.exe experiments/run_benchmarks.py --seed 42 --shots 512 --output experiments/results/benchmark-new-run.json
.venv/Scripts/python.exe experiments/verify_results.py experiments/results/qaoa-new-run.json experiments/results/benchmark-new-run.json
```

If `py` is not on PATH, invoke the installed launcher or Python executable by its full quoted path. On this host, discovery used `C:\Users\ua910\AppData\Local\Programs\Python\Launcher\py.exe -0p`; the interpreter was `C:\Users\ua910\AppData\Local\Programs\Python\Python312\python.exe`. No existing interpreter was modified or uninstalled.

Equivalent Linux/macOS commands (not executed in this local Windows validation), from the repository root:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install --index-url https://pypi.org/simple -r backend/requirements.lock.txt
python -m pip install --no-deps --no-build-isolation -e 'backend[dev]'
python -m pip check
python -m pytest -q backend/tests
python -m raasta.quantum --scenario flood_baseline --budget 9 --shots 512 --seed 42 --output experiments/results/qaoa-new-run.json
python experiments/run_benchmarks.py --seed 42 --shots 512 --output experiments/results/benchmark-new-run.json
```

Use a new output filename for each run: measured outputs are never silently overwritten. `--p 2` enables a second QAOA layer; `--maxiter` bounds COBYLA evaluations. Default seed 42, p=1, shots=512, maxiter=60. The implementation uses exact statevector expectations for optimization and Aer measurement shots for the final distribution. All nine recorded benchmark runs hit the evaluation limit without convergence; warnings disclose this. A console charset warning on Windows may report UTF-8 fallback for circuit drawing; saved JSON is explicitly UTF-8.

## Local execution status

**86 tests passed** in the user's Python 3.12.10 environment. The acceptance QAOA run and nine benchmark cases executed locally with real measurement counts. See `docs/MODEL.md` and the recorded JSON in `experiments/results/`. Default flood/budget 9: best observed `011100`, utility 96, 87.5% feasible samples, 512 shots, zero absolute gap to exact. This is a single seeded, noiseless, six-qubit simulator result, not evidence of quantum advantage.

The earlier Codex-bundled Python environment was blocked by Windows Application Control. Using the user's installed Python resolved execution without modifying security settings. No cloud validation was used.

Classical-only validation remains available explicitly:

```powershell
.venv/Scripts/python.exe -m pytest -q backend/tests/test_model.py
.venv/Scripts/python.exe experiments/run_benchmarks.py --classical-only --output experiments/results/classical-new-run.json
```

This mode does not claim or substitute quantum results. The full-quantum and classical Windows commands were executed locally.

## Module boundaries

- `schema.py`, `scenarios.py`: immutable canonical types and three synthetic fixtures.
- `evaluator.py`: sole authority for feasibility, service logic, and score.
- `exact.py`: exhaustive ground truth over 64 states.
- `greedy.py`: positive marginal utility/cost with decision trace.
- `energy.py`: all-state diagonal Hamiltonian and proved feasibility penalty.
- `quantum.py`: verified circuit construction, optimizer, measurement, and evidence CLI.
- `provenance.py`: actual environment, time, package versions, and source hashes.

No runtime advantage is claimed. Construction and exact statevector simulation both scale exponentially. See the model document for scientific limitations and API sources.

## Phase 3 local API

From the repository root, after installing the lockfile and editable backend:

```powershell
.venv/Scripts/python.exe -m uvicorn raasta.api:app --host 127.0.0.1 --port 8000
```

Swagger: http://127.0.0.1:8000/docs . Health: /api/health . Scenarios: /api/scenarios . POST /api/optimize accepts scenario_id, budget, algorithm, seed, shots and p. Default CORS permits localhost:3000 and 127.0.0.1:3000; override with comma-separated CORS_ORIGINS. No credentials required. API calls use the unchanged Phase 1 solvers. Timeout is 25 seconds; a worker can continue its bounded evaluations after an HTTP timeout.
