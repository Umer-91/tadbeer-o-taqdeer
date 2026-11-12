# Phase 2 verification — 2026-11-12

Checked the locally built production site at `http://127.0.0.1:3000` using the in-app browser on Windows. The HTTP readiness check returned **200**. No backend was running.

## Automated checks

- `npm run lint`: passed.
- `npm run typecheck`: passed.
- `npm test`: **11 passed**, including the actual recorded Phase 1 Qiskit response, request identity, canonical bitstrings/actions, empty unsuccessful results, malformed diagnostics, POST serialization, cancellation, and HTTP/network errors.
- `npm run build`: passed with Next.js 16.4.6/Turbopack; `/` prerendered successfully. The first sandboxed build failed to start a worker; running the same build with approved process permissions succeeded.
- Dependency audit after compatibility/security fixes: **0 vulnerabilities**. Node 24.22.1; npm 12.2.2; TypeScript 6.0.3; ESLint 9.39.5. ESLint 9's upstream end-of-support is documented in the frontend README.

## Observed browser behavior

| Check | Observation |
|---|---|
| 1440×900 desktop | Hero and dashboard inspected; no horizontal document overflow |
| 1280×800 laptop | Hero and dashboard inspected; no horizontal document overflow |
| 390×844 mobile | Hero, stacked controls, network, and results inspected; no horizontal document overflow |
| Urdu | `document.fonts` loaded; Noto Nastaliq Urdu font check passed; exact Unicode text, RTL direction, connected shapes, and spacing inspected |
| 3D | Meshes visibly render; dragging changes camera angle; village hover exposes its label |
| Story | Scroll changes camera/story state and turns damaged network segments coral |
| 2D fallback | Explicit 3D→2D→3D transition verified; application stays usable |
| Dashboard | Scenario selector, keyboard budget adjustment (Home and ArrowRight), Exact radio, parameter expansion, and evidence expansion verified |
| Network access | Hospital activated with Enter; inspector updates; map buttons appear in accessibility tree |
| API failure | Run shows service-unavailable feedback; score remains empty; no plan or quantum result is fabricated |
| Comparison | Disabled until successful Exact and QAOA responses exist |
| Navigation | Hero CTA and dashboard/return links reach their targets |

Initial visual inspection found globally applied focus outlines, tight spacing beneath Nastaliq descenders, and undersized dashboard reading text. These were corrected. Switching off the initial drei HTML label portals produced a `removeChild` cleanup error; labels now use a React-owned overlay. Repeated 3D→2D→3D switching after the fix produced **no new console errors**. A dependency warning remains: R3F uses deprecated `THREE.Clock`; it did not prevent rendering or interactions.

## Evidence

Screenshots are viewport captures; a tall dashboard naturally continues below the fold. They depict synthetic design-preview data, not computed plans.

- [Desktop hero](assets/phase-2/hero-1440x900.jpg)
- [Desktop dashboard](assets/phase-2/dashboard-1440x900.jpg)
- [Shock story](assets/phase-2/shock-1440x900.jpg)
- [Laptop hero](assets/phase-2/hero-1280x800.jpg)
- [Laptop dashboard](assets/phase-2/dashboard-1280x800.jpg)
- [Mobile hero](assets/phase-2/hero-390x844.jpg)
- [Mobile dashboard](assets/phase-2/dashboard-390x844.jpg)
- [Mobile network inspection](assets/phase-2/network-390x844.jpg)
- [Mobile 2D fallback](assets/phase-2/fallback-390x844.jpg)

## Verification limits and Phase 3 work

Live API success, comparative charts with returned data, no-feasible-sample UI, and QASM clipboard copying await real endpoint integration. Boundary tests cover payload validation and unsuccessful-result handling. Browser success was not simulated using fabricated scores.

Reduced-motion CSS/camera handling, hidden-tab pausing, and renderer error boundaries were inspected in source. OS reduced-motion emulation, deliberate GPU context loss, screen-reader speech, measured contrast ratios, and sustained mobile FPS were **not** exercised. The explicit SVG fallback was visually exercised. Do not describe these unmeasured checks as passed.

Phase 3 must provide FastAPI endpoints/CORS, remove scenario preview fallback, exercise real success/error/cancellation paths, verify every interactive control against actual backend responses, and complete the integrated acceptance/report gates.
