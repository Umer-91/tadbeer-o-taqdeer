# Decisions and specification conflicts

## 2026-11-12: Rename only the product branding

The user renamed RAASTA-Q to **TADBEER-O-TAQDEER (تدبیر و تقدیر)**, with tagline **Where Strategy Shapes Destiny.** Repository: `Umer-91/tadbeer-o-taqdeer`. The former acronym is retained as historical context, not as the current product title.

Preserve `backend/raasta`, `python -m raasta.quantum`, and all technical identifiers in the specifications. These are internal module paths rather than public branding. This avoids silently altering architecture or acceptance commands.

All four specifications remain at the repository root, complete. Changes are restricted to the master title, mission branding sentence, repository root name, and branding banners on phase specifications. START_HERE.txt receives the name change; its phase implementation prompts remain future instructions and do not expand the current setup-only task.

## Scaffold before implementation

Follow the master monorepo layout and add shared export directories and cross-component test directories as requested. Do not create fake solver modules, placeholder application endpoints, fabricated results, or untested dependency pins. Package manifests, lockfiles, executable tests, and CI belong to their implementation phases.

No mathematical conflict was identified during setup review. The allowed six-qubit diagonal Hamiltonian approach remains a documented small-instance option, with its exponential construction caveat unchanged. Any later model ambiguity must be recorded and tested against the canonical evaluator.

## 2026-11-12: Urdu identity is a required frontend acceptance criterion

The user's follow-up requires **تدبیر و تقدیر** as the main hero headline, English underneath, Nastaliq with fallback, correct RTL shaping, selectable text, mobile readability, subtle violet reveals, and Urdu in loading/hero/footer. Added these requirements to the master and Phase 2 without removing any original technical content. They will be implemented in Phase 2; the current scope remains setup only.

## Access and release

The supplied repository initially existed as public and empty. Private visibility was subsequently observed in GitHub settings before upload. Git CLI access is independent of connector access; verify the actual transport used. Publishing or submission requires explicit approval. Deadline is 2026-11-12T18:59:00Z; no commits or pushes at/after cutoff.

## Phase 1 implementation decisions — 2026-11-12

- User approved public visibility; GitHub settings subsequently confirmed public. User separately authorized Phase 1. Phases 2 and 3 remain gated.
- Use the explicitly permitted diagonal six-qubit Hamiltonian, with all 64 energy values and primitive gate synthesis recorded. Do not call this a quadratic QUBO or scalable encoding.
- Normalize energies by a positive scale for QAOA phases/optimization; record that scale. It preserves minima.
- For real-valued budgets, choose a penalty from both the utility spread and minimum positive violation. A spread-only bound fails when cost overflow is fractional. The proof and tests are in MODEL.md and test_model.py.
- Keep costs positive integer planning units; budgets may be finite nonnegative real numbers. No rounding tolerances silently expand feasibility.
- Pin the observed Python 3.12.14 environment and installed packages; NumPy/SciPy require Python >=3.12, so the project minimum reflects that.
- Local Windows policy blocks the Qiskit native extension. No security settings changed. The user declined GitHub Actions validation and will provide an approved local environment. Removed the unexecuted CI draft. No Phase 1 commit or push until local quantum validation succeeds; no verified-core claim yet.

### Local environment resolution and circuit export

The user subsequently authorized discovery and use of their installed Python. The launcher was outside PATH; its full path listed Python 3.12.10. A new root `.venv` was created without modifying the installed interpreter or the earlier backend environment. Qiskit/Aer imports, a measured one-qubit smoke circuit, and all 86 tests passed there. Security settings were unchanged; no cloud validation was used.

The first complete test run caught a strict OpenQASM reader rejection of the `sx` gate in exported evidence. Transpile production circuits to standard `u3,cx` instead; a test now checks exported/reloaded circuit statevector equivalence, not merely parsing. All recorded quantum results use this corrected source and include matching source hashes.
