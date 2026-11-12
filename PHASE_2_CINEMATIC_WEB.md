Project: TADBEER-O-TAQDEER (تدبیر و تقدیر) — Where Strategy Shapes Destiny.

# PHASE 2 — CINEMATIC 3D WEBSITE & FUNCTIONAL DASHBOARD
**Prerequisite:** Read MASTER_PLAN.md and Phase 1's `docs/MODEL.md`, `docs/PROGRESS.md`. Do not alter backend optimization logic. This phase builds the visual system and typed API client; Phase 3 connects real endpoints.

## Goal and creative direction
Build a **premium cinematic interactive website**, not a generic admin template. Visual reference: futuristic deep-black Web3-like sites with luminous sculptural 3D, smooth scroll, dramatic typography, physically inspired lighting and restrained particles. Do NOT clone any proprietary site or copy assets. Adapt visual language to a Pakistan-inspired valley and interconnected road/power/water restoration. Landing = dramatic, dashboard = precise and legible. Main benchmark: the judges should understand the disaster story within 10 seconds, and operate the dashboard without instructions.

## Implementation sequence
### Required Urdu brand treatment (user addition, 2026-11-12)
- Main hero headline: **تدبیر و تقدیر**, large and visually striking. Place **TADBEER-O-TAQDEER** underneath and use the exact tagline **Where Strategy Shapes Destiny.**
- Include the Urdu name in the loading sequence, main hero, and footer. Keep the surrounding website primarily English for international hackathon judges.
- Render authentic Unicode Urdu as selectable HTML text with `lang="ur"` and `dir="rtl"` on the Urdu text container. Isolate English text direction as needed. Never generate the Urdu name as an AI image.
- Use a properly rendered Urdu Nastaliq font, with an appropriate Urdu-capable fallback. Verify licensing and the actual loaded font during implementation. Preserve connected letter shapes; do not apply letter spacing or per-letter DOM splitting that disrupts shaping.
- Use subtle violet illumination and cinematic reveal animations on the complete text block; support reduced motion. The identity must feel intentional, premium, culturally authentic, and integral to the design.
- Verify readability and beauty on mobile, with sufficient line height and space for Nastaliq ascenders/descenders. Check font-loading/fallback states, correct RTL order, joined letterforms, and absence of clipping at all required QA sizes. Keep text selectable and accessible throughout reveal animations.

1. Bootstrap `frontend/` Next.js App Router + TypeScript + Tailwind; pin tested dependencies. Add React Three Fiber/Three.js/drei, GSAP ScrollTrigger, Recharts, lucide icons; use shadcn/ui selectively. Make lint/typecheck/build scripts. Do not mix competing animation systems unnecessarily.
2. Define design tokens in CSS: obsidian #06070B, ultraviolet #895CFF, road cyan #48D8F3, power amber #FFBC61, water blue #4A91FF, damage coral #FF5F6D, muted text #9EA4B4. Font: use legally available system or Google Fonts with fallback, editorial display headline and clean UI text. High contrast, no gratuitous glow. UI labels and units precise.
3. Build custom **procedural stylized mountain valley** with low-poly layered terrain, river, bridge, villages, hospital, pump, utility pole/feeder, water pipeline. Use simple instanced meshes/lines; no real geolocation claims. Accessible labels in 2D overlays. Make camera orbit subtle and scroll-based transitions; avoid expensive real-time fluid simulation. Ensure scene is visibly 3D and interactive, not image/video.
4. Create four scroll beats using GSAP ScrollTrigger: `01 / The valley` (healthy network glowing), `02 / The shock` (flood pulse, damage segments turn coral, service indicators dim), `03 / The dependency` (highlight that road+power jointly enable hospital/water), `04 / The response` (camera eases to operational dashboard). Include narrative text short enough to scan. Motion should remain smooth; scrub with scroll and never trap scroll. Use real mouse orbit/hover interactions, touch controls where feasible.
5. Build dashboard layout with (a) dark side rail, (b) scenario selector, (c) budget slider 0–12, (d) algorithm tabs QAOA/exact/greedy, (e) run button, (f) central 2D/3D network map, (g) service-status indicators, (h) action plan and budget use, (i) comparison chart, (j) expandable quantum evidence panel for actual circuit info and measurement distribution. Desktop map-first, mobile stacked panels. Avoid clutter; dashboard is not a second landing page.
6. Implement typed `src/lib/types.ts` exactly matching MASTER_PLAN API. `src/lib/api.ts` uses `NEXT_PUBLIC_API_BASE_URL`, fetches `/api/scenarios` and `/api/optimize`, handles network/validation errors. During frontend-only development, local **fixture JSON** allowed but must display an unmistakable `DESIGN PREVIEW — NOT COMPUTED` label; remove fixture fallback in final integration. Never hardcode claimed quantum scores or recovery numbers.
7. Build component states: initial, loading/progress, success, API failure, no feasible QAOA sample, empty chart. Selected road/power/water link highlights must map to action IDs; dashboard outputs must be derived from response. Include legend, hover tooltips, explanatory side panel, and compare toggle to overlay exact vs QAOA plans (only when both responses exist).
8. Add responsive and accessibility requirements: keyboard navigation, focus rings, contrast, semantic labels, aria-live for run results, `prefers-reduced-motion` static valley view, reduced graphics on mobile, no infinite loading. Prevent WebGL crash from blanking app; provide 2D SVG fallback. Pause animation when tab hidden if feasible. Optimize performance via lazy-load of 3D, geometry reuse, bounded DPR, limited particles, and no huge textures.
9. Add **visual QA**: screenshot at desktop 1440x900, laptop 1280x800, mobile 390x844; check clipping, typography, scroll, readability, scene performance. If screenshots not available, manually inspect via browser tools and record what was/was not checked. No visual claim without inspection.

## Suggested component boundaries
```
src/components/landing/Hero.tsx
src/components/landing/ValleyScene.tsx
src/components/landing/ScrollNarrative.tsx
src/components/dashboard/CommandCenter.tsx
src/components/dashboard/NetworkView.tsx
src/components/dashboard/ScenarioControls.tsx
src/components/dashboard/RestorationPlan.tsx
src/components/dashboard/AlgorithmComparison.tsx
src/components/dashboard/QuantumEvidence.tsx
src/components/shared/StatusPill.tsx
src/lib/types.ts
src/lib/api.ts
```

## Visual quality acceptance
- Landing has **actual** 3D meshes with mouse interaction and scroll-driven state transitions.
- Road/power/water colors are consistent in 3D, dashboard and legends.
- Main CTA `Enter Command Center` works and smoothly navigates to dashboard.
- Dashboard is not merely a mockup: it has stateful controls and real typed fetch client ready for Phase 3.
- User can distinguish illustration vs computed data.
- No layout overflow on mobile; reduced-motion and WebGL fallback work.
- `npm run lint` (if configured), `npm run typecheck`, `npm run build` pass.
- No invented QAOA metrics in production screens.

## Stop condition
Commit `feat: cinematic lifeline experience and dashboard UI`. Update PROGRESS.md with screenshots/tests and explicit API integration TODOs. Do not touch backend or report. Do not spend hours polishing particles if the core dashboard cannot render response data.

## Codex handoff prompt
'Implement PHASE_2_CINEMATIC_WEB.md, following MASTER_PLAN.md and the exact backend model/API contract. Work only in frontend and design docs. Build genuine interactive 3D scroll scenes and a beautiful functional dashboard, with explicit preview labeling until Phase 3. Run build/typecheck and visually verify responsive states. Stop at Phase 2 gate.'
