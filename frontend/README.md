# Tadbeer-o-Taqdeer frontend

Next.js App Router, TypeScript, React Three Fiber/Three.js, GSAP ScrollTrigger, and a typed fetch client. The Urdu brand **تدبیر و تقدیر** is selectable RTL HTML, rendered with self-hosted Noto Nastaliq Urdu. English is the main interface language.

## Run locally

Use Node **24 LTS** (tested: 24.22.1) and npm (tested: 12.2.2). From this directory:

```sh
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run start
```

Open http://127.0.0.1:3000. Use `npm run dev` for live editing. Stop the foreground server with Ctrl+C. On the author's Windows host npm was installed only in ignored `.tools/npm/package`; the equivalent invocation is `node C:\Hackathon\.tools\npm\package\bin\npm-cli.js run dev`. Existing system installations were not changed.

The sandbox blocked Next.js child-process startup; the same production build passed outside that sandbox. No Windows security settings were changed.

## API boundary

Copy `.env.example` to `.env.local` if the API address differs from `http://127.0.0.1:8000`. `NEXT_PUBLIC_API_BASE_URL` is public browser configuration, never a secret. Restart/rebuild after changing it.

- `GET /api/scenarios`: the canonical six-action scenarios.
- `POST /api/optimize`: `{scenario_id, budget, algorithm, seed?, shots?, p?}`.
- The client validates response identity, canonical action ordering, nullable unsuccessful results, and diagnostic ranges. Backend evaluation remains authoritative.
- Scenario-only fixtures are explicitly labeled **DESIGN PREVIEW — NOT COMPUTED** while disconnected. They contain no solver outputs.
- Offline runs show an error. QAOA failure does not substitute an exact solution. Results are cleared when inputs change and before a rerun; request cancellation and a 30-second timeout are supported.
- Comparison becomes available only after Exact and QAOA return successful responses for the same scenario and budget.

Phase 3 must implement the API/CORS, remove the scenario fixture fallback for final integration, and verify real end-to-end success, cancellation, and failure behavior. No HTTP backend was implemented in Phase 2.

## Verification and design

`npm test` exercises the client boundary, including reading the actual committed Phase 1 Qiskit acceptance record. Test payloads never enter the application bundle. See [visual QA](../docs/FRONTEND_QA.md), [design and licenses](../docs/FRONTEND_DESIGN.md), and [progress](../docs/PROGRESS.md).

Direct versions and transitive dependencies are pinned in `package-lock.json`. TypeScript 6.0.3 and ESLint 9.39.5 match the installed Next.js lint plugins; ESLint 9 is upstream end-of-support, so revisit this when those plugins support ESLint 10. A scoped minimatch 11.0.1 override fixes the parser's glob amplification advisory; the complete lint/typecheck/test/build gates passed with it. Do not force dependency upgrades without rerunning those checks.

## Phase 3 integration checkpoint

The frontend now fetches scenarios from the running FastAPI service. No preview scenario is substituted if loading fails. Start the backend in another terminal with `.venv/Scripts/python.exe -m uvicorn raasta.api:app --host 127.0.0.1 --port 8000` from the repository root. Then run the frontend as above. Live browser verification remains pending; see docs/FINAL_STATUS.md.
