# Reproducible experiments

`results/` contains actual measured JSON/CSV outputs only:

- `classical-windows-seed42.json`: historical exact/greedy results from the earlier Python 3.12.14 environment. Its recorded source hashes reflect that earlier source revision, before the circuit export correction. Classical algorithms are deterministic and use no randomness.
- `qaoa-flood-local-python31210-seed42.json`: verified real acceptance run on the user's Python 3.12.10, p=1, seed 42, 512 Aer shots.
- `benchmark-local-python31210-seed42.json`: all three scenarios and budgets 6, 9, 12, with exact, greedy, and genuine QAOA results. All nine cases retained; no seed selection after results. Every optimizer reached its 60-evaluation cap without convergence, as disclosed in each record.

`run_benchmarks.py --classical-only --output <new-file>` explicitly runs the classical algorithms. Without that flag, it requires real Qiskit/Aer execution for every case and fails visibly if unavailable. There is no automatic classical fallback. Each run records environment/source hashes and timestamps; quantum runs additionally record counts, parameter trace, circuit evidence, feasibility, and gaps. Output files are never silently overwritten.

Use `python experiments/verify_results.py <quantum-json> <benchmark-json>` from the root in the approved environment to verify all recorded scores, counts, feasible sample rates, strict OpenQASM circuit replay, and current source hashes. Historical results with different source hashes must be checked against their recorded revision, not silently relabeled as current measurements. File paths and exact commands are in backend/README.md.
