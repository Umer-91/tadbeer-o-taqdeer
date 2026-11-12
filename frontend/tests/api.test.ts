import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createApi, parseResult, parseScenarios } from "../src/lib/api.ts";
import type { OptimizeRequest } from "../src/lib/types.ts";

const request: OptimizeRequest = {
  scenario_id: "flood_baseline",
  budget: 9,
  algorithm: "exact",
};
// This is a contract test payload, never imported by the application.
const result = () => ({
  ...request,
  status: "ok",
  selected_actions: ["temporary_crossing", "hospital_road", "feeder_repair"],
  bitstring: "011100",
  feasible: true,
  utility: 96,
  total_cost: 8,
  metrics: {
    hospital_operational: true,
    water_operational: true,
    basic_connectivity: true,
    hospital_power: true,
  },
  diagnostics: { runtime_ms: 1 },
  warnings: [],
});
const fixtures = JSON.parse(
  readFileSync(
    new URL("../src/lib/scenarios.preview.json", import.meta.url),
    "utf8",
  ),
);
test("accepts the actual Phase 1 Qiskit record without rewriting results", () => {
  const measured = JSON.parse(
    readFileSync(
      new URL(
        "../../experiments/results/qaoa-flood-local-python31210-seed42.json",
        import.meta.url,
      ),
      "utf8",
    ),
  ).result;
  const parsed = parseResult(measured, {
    scenario_id: measured.scenario_id,
    budget: measured.budget,
    algorithm: "qaoa",
  });
  assert.equal(parsed, measured);
  assert.equal(
    parsed.diagnostics.distribution?.reduce((sum, row) => sum + row.count, 0),
    parsed.diagnostics.shots,
  );
});
test("scenario fixtures contain only the canonical six interventions", () => {
  assert.equal(parseScenarios(fixtures).length, 3);
  const invalid = structuredClone(fixtures);
  invalid[0].actions.reverse();
  assert.throws(() => parseScenarios(invalid), /invalid intervention/);
});
test("accepts a matching response without changing reported values", () => {
  const input = result();
  assert.equal(parseResult(input, request), input);
});
test("rejects responses from stale requests", () => {
  for (const change of [
    { budget: 6 },
    { scenario_id: "bridge_blocked" },
    { algorithm: "qaoa" },
  ])
    assert.throws(
      () => parseResult({ ...result(), ...change }, request),
      /does not match/,
    );
});
test("rejects malformed or infeasible success claims", () => {
  for (const change of [
    { total_cost: 10 },
    { feasible: false },
    { utility: NaN },
    { bitstring: "01110" },
    { selected_actions: ["bridge_repair"] },
    { metrics: null },
  ])
    assert.throws(() => parseResult({ ...result(), ...change }, request));
});
test("no feasible sample stays empty, without an exact replacement", () => {
  const empty = {
    ...result(),
    status: "no_feasible_sample",
    selected_actions: [],
    bitstring: null,
    feasible: null,
    utility: null,
    total_cost: null,
    metrics: null,
  };
  assert.equal(parseResult(empty, request).utility, null);
  assert.throws(
    () => parseResult({ ...empty, utility: 96 }, request),
    /unsuccessful computation/,
  );
});
test("rejects invalid measurement diagnostics", () => {
  for (const diagnostics of [
    { runtime_ms: -1 },
    { runtime_ms: 1, feasible_sample_rate: 2 },
    {
      runtime_ms: 1,
      distribution: [{ bitstring: "111111", count: -1, probability: 0.5 }],
    },
  ])
    assert.throws(() => parseResult({ ...result(), diagnostics }, request));
});
test("API sends the exact requested parameters and validates its response", async () => {
  let url = "";
  let sent: RequestInit | undefined;
  const fake: typeof fetch = async (input, init) => {
    url = String(input);
    sent = init;
    return Response.json(result());
  };
  const received = await createApi("http://local.test/", fake).optimize(
    request,
  );
  assert.equal(url, "http://local.test/api/optimize");
  assert.equal(sent?.method, "POST");
  assert.deepEqual(JSON.parse(String(sent?.body)), request);
  assert.equal(received.utility, 96);
});
test("network failure surfaces an error instead of returning a fixture score", async () => {
  const fake: typeof fetch = async () => {
    throw new TypeError("Failed to fetch");
  };
  await assert.rejects(
    createApi("http://local.test", fake).optimize(request),
    /No result has been generated/,
  );
});
test("HTTP validation errors and unreadable JSON remain explicit", async () => {
  await assert.rejects(
    createApi(
      "http://local.test",
      async () => new Response("invalid", { status: 422 }),
    ).optimize(request),
    /rejected these settings/,
  );
  await assert.rejects(
    createApi(
      "http://local.test",
      async () => new Response("invalid"),
    ).optimize(request),
    /unreadable JSON/,
  );
});
test("cancellation reaches fetch and does not produce a result", async () => {
  const controller = new AbortController();
  controller.abort();
  const fake: typeof fetch = async (_, init) => {
    assert.equal(init?.signal?.aborted, true);
    throw new DOMException("Aborted", "AbortError");
  };
  await assert.rejects(
    createApi("http://local.test", fake).optimize(request, controller.signal),
    /cancelled/,
  );
});
