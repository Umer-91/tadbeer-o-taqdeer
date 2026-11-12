"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  Activity,
  ArrowUpRight,
  Atom,
  Check,
  CircleHelp,
  Droplets,
  GitCompareArrows,
  Layers,
  LoaderCircle,
  Play,
  Radio,
  RefreshCw,
  Route,
  Settings2,
  ShieldCheck,
  Square,
  Zap,
} from "lucide-react";
import { createApi } from "@/lib/api";
import type { Algorithm, Scenario, SolverResult } from "@/lib/types";

import NetworkView from "./NetworkView";
import AlgorithmComparison from "./AlgorithmComparison";
import QuantumEvidence from "./QuantumEvidence";


const api = createApi();
const algorithms: { id: Algorithm; name: string; description: string }[] = [
  { id: "qaoa", name: "QAOA", description: "Sample a six-qubit circuit" },
  { id: "exact", name: "Exact", description: "Enumerate all 64 choices" },
  {
    id: "greedy",
    name: "Greedy",
    description: "Follow marginal utility per cost",
  },
];

export default function CommandCenter() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]),
    [connected, setConnected] = useState(false),
    [connecting, setConnecting] = useState(true);
  const [scenarioId, setScenarioId] = useState(""),
    [budget, setBudget] = useState(9),
    [algorithm, setAlgorithm] = useState<Algorithm>("qaoa");
  const [results, setResults] = useState<
      Partial<Record<Algorithm, SolverResult>>
    >({}),
    [error, setError] = useState<string | null>(null),
    [busy, setBusy] = useState(false);
  const [compare, setCompare] = useState(false),
    [showPlan, setShowPlan] = useState(false),
    [settings, setSettings] = useState(false),
    [shots, setShots] = useState(512),
    [seed, setSeed] = useState(42),
    [depth, setDepth] = useState(1);
  const active = useRef<AbortController | null>(null),
    connection = useRef<AbortController | null>(null);
  const scenario = scenarios.find((s) => s.id === scenarioId) ?? scenarios[0];
  const result = results[algorithm];
  const loadScenarios = useCallback(async () => {
    connection.current?.abort();
    const controller = new AbortController();
    connection.current = controller;
    try {
      const data = await api.scenarios(controller.signal);
      if (controller.signal.aborted) return;
      setScenarios(data);
      setConnected(true);
      setScenarioId((current) =>
        data.some((s) => s.id === current) ? current : data[0].id,
      );
      setResults({});
      setCompare(false);
      setError(null);
    } catch {
      if (!controller.signal.aborted) setConnected(false);
    } finally {
      if (!controller.signal.aborted) setConnecting(false);
    }
  }, []);
  useEffect(() => {
    // This subscribes to asynchronous fetch completion; no state is set before the await.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadScenarios();
    return () => {
      connection.current?.abort();
      active.current?.abort();
    };
  }, [loadScenarios]);
  function reset() {
    active.current?.abort();
    setResults({});
    setError(null);
    setCompare(false);
  }
  async function run() {
    active.current?.abort();
    const controller = new AbortController();
    active.current = controller;
    setBusy(true);
    setError(null);
    setCompare(false);
    setShowPlan(false);
    setResults((previous) => ({ ...previous, [algorithm]: undefined }));
    try {
      const response = await api.optimize(
        {
          scenario_id: scenario.id,
          budget,
          algorithm,
          ...(algorithm === "qaoa" ? { seed, shots, p: depth } : {}),
        },
        controller.signal,
      );
      if (controller.signal.aborted) return;
      setResults((previous) => ({ ...previous, [algorithm]: response }));
      setShowPlan(true);
      if (response.status === "error")
        setError(
          response.warnings.join(" ") ||
            "The service could not complete this computation.",
        );
    } catch (cause) {
      if (!controller.signal.aborted)
        setError(
          cause instanceof Error
            ? cause.message
            : "Unable to run the computation.",
        );
    } finally {
      if (active.current === controller) setBusy(false);
    }
  }
  if (!scenario) return <section id="command-center" className="command-section section-pad"><h2>The command center</h2><p role="status">{connecting ? "Connecting to the computation service…" : "Computation service unavailable. Start the backend and reconnect. No scenarios or results have been substituted."}</p><button className="primary-button" disabled={connecting} onClick={() => {setConnecting(true); void loadScenarios();}}>Reconnect</button></section>;
  const canCompare =
    algorithm !== "greedy" &&
    results.qaoa?.status === "ok" &&
    results.exact?.status === "ok";
  const serviceMetrics = [
    {
      key: "basic_connectivity" as const,
      label: "Road access",
      icon: Route,
      color: "road",
    },
    {
      key: "hospital_power" as const,
      label: "Hospital power",
      icon: Zap,
      color: "power",
    },
    {
      key: "water_operational" as const,
      label: "Water service",
      icon: Droplets,
      color: "water",
    },
    {
      key: "hospital_operational" as const,
      label: "Hospital care",
      icon: Activity,
      color: "violet",
    },
  ];
  return (
    <section
      id="command-center"
      className="command-section section-pad"
      aria-labelledby="command-heading"
    >
      <div className="command-intro">
        <div>
          <span className="eyebrow">
            <i /> FROM UNDERSTANDING TO ACTION
          </span>
          <h2 id="command-heading">
            The command center<span>.</span>
          </h2>
          <p>
            Explore the trade-offs. Inspect the evidence. Make every planning
            unit count.
          </p>
        </div>
        <span className="research-stamp">
          <ShieldCheck size={16} /> SYNTHETIC RESEARCH PROTOTYPE
        </span>
      </div>
      <div className="command-shell">
        <aside className="command-rail" aria-label="Workspace sections">
          <a
            className="active"
            href="#command-heading"
            aria-label="Restoration planning"
          >
            <Layers size={20} />
          </a>
          <a href="#results-panel" aria-label="Restoration results">
            <Activity size={20} />
          </a>
          <a href="#evidence-section" aria-label="Quantum evidence">
            <Atom size={20} />
          </a>
          <a href="#method" aria-label="About the model">
            <CircleHelp size={20} />
          </a>
          <span className="rail-line" />
          <span className="rail-label">T—Q</span>
        </aside>
        <div className="command-main">
          <div className="command-topbar">
            <span>
              <Radio size={14} /> RESTORATION WORKSPACE <b>/ 01</b>
            </span>
            <span className={connected ? "connection online" : "connection"}>
              <i />
              {connected ? "Service connected" : "Service offline"}
              <button
                onClick={() => {
                  setConnecting(true);
                  void loadScenarios();
                }}
                disabled={connecting || busy}
                aria-label="Reconnect computation service"
              >
                <RefreshCw size={12} className={connecting ? "spin" : ""} />
              </button>
            </span>
          </div>
          {!connected && (
            <div className="preview-banner">
              <span>DESIGN PREVIEW — NOT COMPUTED</span>
              <small>
                Scenario fixtures are shown. Optimization requires the backend
                connection.
              </small>
            </div>
          )}
          <div className="workspace-grid">
            <section
              className="controls-panel"
              aria-label="Scenario and optimization controls"
            >
              <div className="panel-heading">
                <h3>Plan your response</h3>
                <span>01—06</span>
              </div>
              <label className="field-label" htmlFor="scenario">
                DISASTER SCENARIO
              </label>
              <select
                id="scenario"
                value={scenario.id}
                disabled={busy}
                onChange={(e) => {
                  reset();
                  setScenarioId(e.target.value);
                  setBudget(
                    scenarios.find((s) => s.id === e.target.value)
                      ?.budget_default ?? 9,
                  );
                }}
              >
                {scenarios.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name.replace("Synthetic ", "")}
                  </option>
                ))}
              </select>
              <p className="scenario-description">{scenario.description}</p>
              <div className="budget-heading">
                <label className="field-label" htmlFor="budget">
                  AVAILABLE BUDGET
                </label>
                <span>
                  <b>{budget}</b> / 12
                </span>
              </div>
              <input
                id="budget"
                aria-valuetext={`${budget} abstract planning units`}
                type="range"
                min="0"
                max="12"
                step="1"
                value={budget}
                disabled={busy}
                style={
                  {
                    "--range": `${(budget / 12) * 100}%`,
                  } as React.CSSProperties
                }
                onChange={(e) => {
                  reset();
                  setBudget(Number(e.target.value));
                }}
              />
              <div className="range-labels">
                <span>0</span>
                <span>PLANNING UNITS · NOT PKR</span>
                <span>12</span>
              </div>
              <fieldset className="algorithm-fieldset" disabled={busy}>
                <legend className="field-label">OPTIMIZATION METHOD</legend>
                {algorithms.map((a) => (
                  <label
                    className={`algorithm-choice ${algorithm === a.id ? "selected" : ""}`}
                    key={a.id}
                  >
                    <input
                      type="radio"
                      name="algorithm"
                      value={a.id}
                      checked={algorithm === a.id}
                      onChange={() => {
                        setAlgorithm(a.id);
                        setError(null);
                        setCompare(false);
                        setShowPlan(results[a.id]?.status === "ok");
                      }}
                    />
                    <span>
                      {a.id === "qaoa" ? (
                        <Atom size={17} />
                      ) : a.id === "exact" ? (
                        <ShieldCheck size={17} />
                      ) : (
                        <Route size={17} />
                      )}
                    </span>
                    <span>
                      <b>{a.name}</b>
                      <small>{a.description}</small>
                    </span>
                    <i />
                  </label>
                ))}
              </fieldset>
              <button
                className="settings-toggle"
                onClick={() => setSettings((v) => !v)}
                aria-expanded={settings}
                aria-controls="quantum-settings"
              >
                <Settings2 size={13} /> Quantum parameters{" "}
                <span>{settings ? "−" : "+"}</span>
              </button>
              {settings && (
                <div id="quantum-settings" className="advanced-settings">
                  <label>
                    Shots
                    <select
                      value={shots}
                      disabled={busy}
                      onChange={(e) => {
                        reset();
                        setShots(Number(e.target.value));
                      }}
                    >
                      {[128, 256, 512, 1024, 2048].map((n) => (
                        <option key={n}>{n}</option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Seed
                    <input
                      type="number"
                      value={seed}
                      min="0"
                      max="4294967295"
                      disabled={busy}
                      onChange={(e) => {
                        reset();
                        setSeed(
                          Math.max(
                            0,
                            Math.min(
                              4294967295,
                              Math.floor(Number(e.target.value)),
                            ),
                          ),
                        );
                      }}
                    />
                  </label>
                  <label>
                    QAOA layers
                    <select
                      value={depth}
                      disabled={busy}
                      onChange={(e) => {
                        reset();
                        setDepth(Number(e.target.value));
                      }}
                    >
                      <option value="1">p = 1</option>
                      <option value="2">p = 2</option>
                    </select>
                  </label>
                </div>
              )}
              <button
                className="run-button"
                onClick={() => void run()}
                disabled={busy || connecting}
              >
                {busy ? (
                  <LoaderCircle className="spin" size={16} />
                ) : (
                  <Play size={15} fill="currentColor" />
                )}
                {busy ? "Running computation…" : "Run optimization"}
                <ArrowUpRight size={15} />
              </button>
              {busy && (
                <button
                  className="cancel-button"
                  onClick={() => {
                    active.current?.abort();
                    setBusy(false);
                    setError(
                      "Request cancelled. No new result has been generated.",
                    );
                  }}
                >
                  <Square size={10} /> Cancel request
                </button>
              )}
              <p className="control-footnote">
                <ShieldCheck size={12} /> Every reported plan is checked for
                feasibility.
              </p>
            </section>
            <section
              className="network-panel"
              aria-label="Infrastructure network"
            >
              <div className="panel-heading">
                <div>
                  <span className="eyebrow">THE CONNECTED VALLEY</span>
                  <h3>One landscape. Three lifelines.</h3>
                </div>
                <span className="synthetic-tag">SYNTHETIC DATA</span>
              </div>
              <div className="map-toolbar">
                <div className="segmented-control" aria-label="Network display">
                  <button
                    onClick={() => setShowPlan(false)}
                    aria-pressed={!showPlan}
                  >
                    Before
                  </button>
                  <button
                    onClick={() => setShowPlan(true)}
                    aria-pressed={showPlan}
                    disabled={!result || result.status !== "ok"}
                  >
                    Selected plan
                  </button>
                </div>
                <button
                  className="compare-button"
                  disabled={!canCompare}
                  aria-pressed={compare}
                  onClick={() => setCompare((v) => !v)}
                  title={
                    canCompare
                      ? "Overlay Exact and QAOA interventions"
                      : "Run both Exact and QAOA at the same budget to compare"
                  }
                >
                  <GitCompareArrows size={13} /> Compare
                </button>
              </div>
              <NetworkView
                scenario={scenario}
                selected={
                  result?.status === "ok" ? result.selected_actions : []
                }
                comparison={
                  compare
                    ? algorithm === "exact"
                      ? results.qaoa?.selected_actions
                      : results.exact?.selected_actions
                    : []
                }
                showPlan={showPlan}
              />
              <div className="map-footer">
                <div className="lifeline-legend">
                  <span>
                    <i className="road" /> Roads
                  </span>
                  <span>
                    <i className="power" /> Electricity
                  </span>
                  <span>
                    <i className="water" /> Water
                  </span>
                </div>
                <span>
                  {compare
                    ? "VIOLET OUTLINE: COMPARISON PLAN"
                    : "HOVER / FOCUS TO INSPECT"}
                </span>
              </div>
            </section>
            <section
              id="results-panel"
              className="results-panel"
              aria-label="Computed restoration results"
            >
              <div className="panel-heading">
                <h3>Restoration outlook</h3>
                <span
                  className={`result-state ${result?.status === "ok" ? "has-result" : ""}`}
                >
                  {busy
                    ? "RUNNING"
                    : result?.status === "ok"
                      ? "COMPUTED"
                      : "AWAITING RUN"}
                </span>
              </div>
              <div className="score-block">
                <span className="field-label">WEIGHTED SERVICE SCORE</span>
                <div>
                  {result?.status === "ok" ? result.utility?.toFixed(1) : "—"}
                  <small>UTILITY</small>
                </div>
                <p>
                  {result?.status === "ok"
                    ? `${result.total_cost} of ${budget} planning units used`
                    : "A score appears after a verified computation."}
                </p>
              </div>
              <div className="service-list">
                {serviceMetrics.map(({ key, label, icon: Icon, color }) => (
                  <div key={key}>
                    <span>
                      <Icon size={15} className={color} />
                      {label}
                    </span>
                    <span
                      className={
                        result?.metrics?.[key]
                          ? "service-restored"
                          : "service-pending"
                      }
                    >
                      {result?.metrics
                        ? result.metrics[key]
                          ? "Restored"
                          : "Not restored"
                        : "Not computed"}
                    </span>
                  </div>
                ))}
              </div>
              <div className="action-plan">
                <div className="panel-heading">
                  <h3>Selected interventions</h3>
                  <span>{result?.selected_actions.length ?? 0}</span>
                </div>
                {result?.status === "ok" ? (
                  result.selected_actions.length ? (
                    result.selected_actions.map((id) => (
                      <div className="selected-action" key={id}>
                        <Check size={12} />
                        <span>
                          {scenario.actions.find((a) => a.id === id)?.label}
                        </span>
                        <b>{scenario.actions.find((a) => a.id === id)?.cost}</b>
                      </div>
                    ))
                  ) : (
                    <p className="fine-print">
                      The feasible plan selects no interventions.
                    </p>
                  )
                ) : (
                  <p className="empty-plan">
                    Your restoration portfolio will appear here.
                    <br />
                    No interventions have been computed.
                  </p>
                )}
              </div>
              <AlgorithmComparison results={results} />
            </section>
          </div>
          <div className="run-feedback" role="status" aria-live="polite">
            {error && (
              <p className="error-notice">
                <b>Unable to complete this run.</b> {error}
                <button onClick={() => void run()} disabled={busy}>
                  Retry
                </button>
              </p>
            )}
            {result?.status === "no_feasible_sample" && (
              <p className="notice">
                <b>No feasible sample was measured.</b> Try a different seed or
                more shots. An exact solution has not been substituted.
              </p>
            )}
            {result?.status === "ok" && (
              <p className="success-notice">
                Plan computed by {result.algorithm.toUpperCase()} in{" "}
                {result.diagnostics.runtime_ms.toFixed(1)} ms.{" "}
                {result.diagnostics.feasible_sample_rate !== undefined &&
                  `${(result.diagnostics.feasible_sample_rate * 100).toFixed(1)}% feasible samples.`}
              </p>
            )}
            {result?.warnings.map((w, i) => (
              <p className="result-warning" key={i}>
                {w}
              </p>
            ))}
          </div>
          <div id="evidence-section">
            <QuantumEvidence result={results.qaoa} />
          </div>
          <div className="workspace-footnote">
            <span>FICTIONAL DATA. REAL QUESTIONS.</span>
            <p>
              Service scores are abstract weights, not people saved. This
              prototype does not control real infrastructure.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
