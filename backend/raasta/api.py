"""Local research API using the unchanged Phase 1 solvers."""
import asyncio
import importlib
import logging
import os
import threading
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from .exact import solve_exact
from .greedy import solve_greedy
from .scenarios import get_scenario, list_scenarios


class OptimizeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    scenario_id: str
    budget: float = Field(ge=0, le=12, allow_inf_nan=False)
    algorithm: Literal["exact", "greedy", "qaoa"]
    seed: int = Field(default=42, ge=0, le=4294967295)
    shots: int = Field(default=512, ge=1, le=2048)
    p: int = Field(default=1, ge=1, le=2)


class OptimizeResponse(BaseModel):
    scenario_id: str
    algorithm: Literal["exact", "greedy", "qaoa"]
    budget: float
    status: Literal["ok", "no_feasible_sample"]
    selected_actions: list[str]
    bitstring: str | None
    feasible: bool | None
    utility: float | None
    total_cost: float | None
    metrics: dict[str, bool] | None
    diagnostics: dict[str, Any]
    warnings: list[str]


app = FastAPI(title="Tadbeer-o-Taqdeer", version="0.3.0")
COMPUTE_TIMEOUT_SECONDS = 25
_capacity = threading.BoundedSemaphore(2)


def admitted_compute(request: OptimizeRequest):
    # The slot belongs to the actual worker, not the HTTP waiter. A timeout
    # cannot free capacity while the solver is still consuming CPU.
    try:
        return compute(request)
    finally:
        _capacity.release()


origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://127.0.0.1:3000,http://localhost:3000").split(",") if origin.strip()]
if "*" in origins:
    raise ValueError("Explicit frontend origins are required")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.get("/api/health")
def health():
    try:
        importlib.import_module("raasta.quantum")
        available = True
    except (ImportError, OSError):
        available = False
    return {"status": "ok" if available else "degraded", "version": "0.3.0", "qiskit_available": available}


@app.get("/api/scenarios")
def scenarios():
    return [s.to_dict() for s in list_scenarios()]


def compute(request: OptimizeRequest):
    scenario = get_scenario(request.scenario_id)
    if request.algorithm == "exact":
        return solve_exact(scenario, request.budget).to_dict()
    if request.algorithm == "greedy":
        return solve_greedy(scenario, request.budget).to_dict()
    try:
        quantum = importlib.import_module("raasta.quantum")
    except (ImportError, OSError) as exc:
        raise HTTPException(503, "Qiskit execution unavailable") from exc
    return quantum.solve_qaoa(scenario, request.budget, seed=request.seed, shots=request.shots, p=request.p, maxiter=60).to_dict()


@app.post("/api/optimize", response_model=OptimizeResponse)
async def optimize(request: OptimizeRequest):
    try:
        get_scenario(request.scenario_id)
    except (KeyError, ValueError) as exc:
        raise HTTPException(422, "Unknown synthetic scenario") from exc
    if not _capacity.acquire(blocking=False):
        raise HTTPException(503, "Computation capacity busy; retry after the current runs finish", headers={"Retry-After": "2"})
    loop = asyncio.get_running_loop()
    try:
        worker = loop.run_in_executor(None, admitted_compute, request)
    except Exception:
        _capacity.release()
        raise
    # Retrieve late failures even when the HTTP caller has already timed out.
    worker.add_done_callback(lambda task: task.exception() if not task.cancelled() else None)
    try:
        return await asyncio.wait_for(asyncio.shield(worker), timeout=COMPUTE_TIMEOUT_SECONDS)
    except TimeoutError as exc:
        raise HTTPException(504, "Computation exceeded 25 seconds; no result returned") from exc
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Optimization failed")
        raise HTTPException(500, "Computation failed; no substitute result generated") from exc
