# Architecture and ownership

Status: planned, unimplemented. MASTER_PLAN.md remains authoritative.

Next.js/TypeScript browser with React Three Fiber, Three.js and GSAP -> FastAPI -> canonical scenario/schema/evaluator -> Qiskit QAOA, exact enumeration and greedy -> typed JSON -> dashboard and evidence panels.

The optimizer and API share `backend/raasta/`; this avoids duplicating feasibility or objective calculations. `shared/` holds future exports, not a second authority. `frontend/src/lib/` owns the typed API adapter. No real infrastructure is controlled.

The full six-action model, dependency equations, utility, feasibility constraints, bit ordering, and API payloads remain in the complete specifications. This document does not replace them. Cinematic terrain is a synthetic illustration, distinct from measured optimization evidence.

Architecture diagram and report assets will be created in Phase 3 after real implementation and experiments. `docs/assets/` is reserved for supporting assets; final deliverables retain the paths required by MASTER_PLAN.md.
