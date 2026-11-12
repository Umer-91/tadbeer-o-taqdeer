# Development workflow

Read MASTER_PLAN.md and the active phase specification in full. Setup is complete only after remote verification; implementation needs a separate instruction.

## Branches and commits

- Keep `main` stable. Use `phase-1-quantum`, `phase-2-frontend`, and `phase-3-integration` sequentially.
- Before a phase, fetch origin, inspect changes, and fast-forward main only. Create its branch from the updated main; if it already exists, inspect and reuse it without resetting it.
- Run the active phase's acceptance checks. Record exact commands, actual results, limitations, and blockers in `docs/PROGRESS.md`.
- Review `git diff --check`, `git diff --cached`, and `git status` before committing. Stage explicit paths; inspect for secrets and generated dependencies.
- Commit coherent tested work. Use messages such as `feat: verified lifeline optimization core` only when the claim is supported by real tests.
- Push using `git push -u origin <branch>`. Never force-push, rewrite shared history, or overwrite unrelated work.
- After each push, compare `git rev-parse HEAD` with `git ls-remote origin refs/heads/<branch>` and record the verified hash. Review and integrate passing work into main.

## Deadline and access

Before every commit and push, verify that current time is earlier than **2026-11-12T18:59:00Z** (23:59 PKT). Do not commit or push at/after this cutoff. This is a workflow rule, not a server-enforced branch protection rule. Do not make the repository public without explicit user approval. Never store credentials in Git or request tokens in chat.

## Evidence requirements

Phase 1 requires real Qiskit circuits and shot counts, exact 64-state validation, endianness tests, and measured results. Phase 2 requires type/build checks and visual QA. Phase 3 requires API and end-to-end validation and a report based only on measured outputs. No hardcoded frontend optimization results, invented benchmarks, or unsupported quantum advantage claims.

Dependencies and lockfiles must reflect installed and tested versions. Empty setup directories do not constitute tested applications. CI will be added alongside actual test/build commands; no placeholder passing jobs.
