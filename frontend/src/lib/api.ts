import { ACTION_IDS } from "./types.ts";
import type { OptimizeRequest, Scenario, SolverResult } from "./types.ts";

export class ApiError extends Error {
  status: number | undefined;
  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}
const record = (v: unknown): v is Record<string, unknown> =>
  typeof v === "object" && v !== null && !Array.isArray(v);
const finite = (v: unknown): v is number =>
  typeof v === "number" && Number.isFinite(v);
const actionId = (v: unknown) =>
  typeof v === "string" && (ACTION_IDS as readonly string[]).includes(v);
const bits = (v: unknown) => typeof v === "string" && /^[01]{6}$/.test(v);

export function parseScenarios(data: unknown): Scenario[] {
  if (!Array.isArray(data) || !data.length)
    throw new ApiError("The service returned no scenarios.");
  for (const s of data) {
    if (
      !record(s) ||
      typeof s.id !== "string" ||
      typeof s.name !== "string" ||
      typeof s.description !== "string" ||
      s.synthetic !== true ||
      !finite(s.budget_default) ||
      !Array.isArray(s.actions) ||
      s.actions.length !== 6 ||
      !Array.isArray(s.nodes) ||
      !Array.isArray(s.links)
    )
      throw new ApiError(
        "The scenario data does not match the six-action contract.",
      );
    if (
      s.actions.some(
        (a, i) =>
          !record(a) ||
          a.index !== i ||
          a.id !== ACTION_IDS[i] ||
          typeof a.label !== "string" ||
          !finite(a.cost) ||
          a.cost <= 0 ||
          typeof a.enabled !== "boolean",
      )
    )
      throw new ApiError("The service returned an invalid intervention.");
  }
  return data as Scenario[];
}

export function parseResult(
  data: unknown,
  request: OptimizeRequest,
): SolverResult {
  if (
    !record(data) ||
    data.scenario_id !== request.scenario_id ||
    data.algorithm !== request.algorithm ||
    data.budget !== request.budget ||
    !["ok", "no_feasible_sample", "error"].includes(String(data.status))
  )
    throw new ApiError(
      "The result does not match your requested scenario, budget, and algorithm.",
    );
  if (
    !Array.isArray(data.selected_actions) ||
    !data.selected_actions.every(actionId) ||
    new Set(data.selected_actions).size !== data.selected_actions.length ||
    !Array.isArray(data.warnings) ||
    !data.warnings.every((w) => typeof w === "string") ||
    !record(data.diagnostics) ||
    !finite(data.diagnostics.runtime_ms) ||
    data.diagnostics.runtime_ms < 0
  )
    throw new ApiError("The service returned an incomplete result.");
  if (data.status === "ok") {
    if (
      !bits(data.bitstring) ||
      data.feasible !== true ||
      !finite(data.utility) ||
      !finite(data.total_cost) ||
      data.total_cost < 0 ||
      data.total_cost > request.budget ||
      !record(data.metrics) ||
      ![
        "hospital_operational",
        "water_operational",
        "basic_connectivity",
        "hospital_power",
      ].every(
        (k) =>
          typeof (data.metrics as Record<string, unknown>)[k] === "boolean",
      )
    )
      throw new ApiError("The service did not return a valid feasible plan.");
    const selected = ACTION_IDS.filter(
      (_, i) => (data.bitstring as string)[i] === "1",
    );
    if (selected.join() !== data.selected_actions.join())
      throw new ApiError(
        "Selected actions do not match the canonical bitstring.",
      );
  } else if (
    [
      data.bitstring,
      data.feasible,
      data.utility,
      data.total_cost,
      data.metrics,
    ].some((v) => v !== null) ||
    data.selected_actions.length
  )
    throw new ApiError(
      "An unsuccessful computation must not contain a claimed solution.",
    );
  const d = data.diagnostics;
  for (const k of [
    "shots",
    "depth",
    "gate_count",
    "optimizer_evaluations",
    "exact_optimum",
    "optimality_gap",
  ])
    if (d[k] !== undefined && d[k] !== null && !finite(d[k]))
      throw new ApiError("Invalid computation diagnostics.");
  if (
    d.feasible_sample_rate !== undefined &&
    (!finite(d.feasible_sample_rate) ||
      d.feasible_sample_rate < 0 ||
      d.feasible_sample_rate > 1)
  )
    throw new ApiError("Invalid feasible sample rate.");
  if (
    d.distribution !== undefined &&
    (!Array.isArray(d.distribution) ||
      d.distribution.some(
        (row) =>
          !record(row) ||
          !bits(row.bitstring) ||
          !finite(row.probability) ||
          row.probability < 0 ||
          row.probability > 1 ||
          !Number.isInteger(row.count) ||
          (row.count as number) < 0,
      ))
  )
    throw new ApiError("Invalid measurement distribution.");
  return data as unknown as SolverResult;
}

export function createApi(
  base = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000",
  fetcher: typeof fetch = fetch,
) {
  async function request(
    path: string,
    init: RequestInit = {},
    signal?: AbortSignal,
  ): Promise<unknown> {
    const controller = new AbortController();
    const abort = () => controller.abort();
    if (signal?.aborted) controller.abort();
    signal?.addEventListener("abort", abort, { once: true });
    const timeout = setTimeout(() => controller.abort(), 30_000);
    try {
      const response = await fetcher(`${base.replace(/\/$/, "")}${path}`, {
        ...init,
        signal: controller.signal,
        headers: { "Content-Type": "application/json", ...init.headers },
      });
      if (!response.ok)
        throw new ApiError(
          response.status === 422
            ? "The service rejected these settings. Check the scenario and run parameters."
            : `The computation service returned ${response.status}. Please retry.`,
          response.status,
        );
      try {
        return await response.json();
      } catch {
        throw new ApiError("The service returned unreadable JSON.");
      }
    } catch (error) {
      if (error instanceof ApiError) throw error;
      if (signal?.aborted) throw new ApiError("Request cancelled.");
      if (controller.signal.aborted)
        throw new ApiError(
          "The service took too long. Please retry with fewer shots.",
        );
      throw new ApiError(
        "Computation service unavailable. Start the FastAPI backend, then reconnect. No result has been generated.",
      );
    } finally {
      clearTimeout(timeout);
      signal?.removeEventListener("abort", abort);
    }
  }
  return {
    scenarios: async (signal?: AbortSignal) =>
      parseScenarios(await request("/api/scenarios", {}, signal)),
    optimize: async (body: OptimizeRequest, signal?: AbortSignal) =>
      parseResult(
        await request(
          "/api/optimize",
          { method: "POST", body: JSON.stringify(body) },
          signal,
        ),
        body,
      ),
  };
}
