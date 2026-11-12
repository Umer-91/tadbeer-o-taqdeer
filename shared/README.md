# Shared data boundary

`scenarios/` is reserved for explicitly synthetic exports and development fixtures. `contracts/` is reserved for generated schema exports from the backend's canonical typed models.

The backend remains the source of truth (`backend/raasta/schema.py` and `scenarios.py`, to be implemented). Do not independently redefine utility, constraints, or scenario semantics here. The frontend's typed API client must match these contracts. No data or schemas have been invented during setup.
