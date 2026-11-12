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
