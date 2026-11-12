"use client";
import { useState } from "react";
import { ChevronDown, Copy, Check, Atom } from "lucide-react";
import type { SolverResult } from "@/lib/types";
export default function QuantumEvidence({ result }: { result?: SolverResult }) {
  const [open, setOpen] = useState(false),
    [copied, setCopied] = useState(false);
  const d = result?.algorithm === "qaoa" ? result.diagnostics : undefined;
  const rows = d?.distribution
    ? [...d.distribution].sort((a, b) => b.count - a.count).slice(0, 8)
    : [];
  async function copy() {
    if (!d?.compiled_qasm2) return;
    try {
      await navigator.clipboard.writeText(d.compiled_qasm2);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  }
  return (
    <section className="evidence-panel">
      <button
        className="evidence-toggle"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls="quantum-evidence"
      >
        <span>
          <Atom size={17} />
          <b>Quantum evidence</b>
          <small>
            {d
              ? "Measured circuit & distribution"
              : "The computation, made inspectable"}
          </small>
        </span>
        <ChevronDown size={16} className={open ? "rotate" : ""} />
      </button>
      {open && (
        <div id="quantum-evidence" className="evidence-content">
          {!d ? (
            <div className="empty-evidence">
              <Atom size={26} />
              <p>No quantum measurement yet.</p>
              <span>
                Run QAOA with the computation service connected to inspect real
                shots, circuit depth, and the sampled distribution.
              </span>
            </div>
          ) : (
            <>
              <div className="evidence-stats">
                {[
                  ["SHOTS", d.shots],
                  ["DEPTH", d.depth],
                  ["GATES", d.gate_count],
                  ["EVALUATIONS", d.optimizer_evaluations],
                ].map(([label, value]) => (
                  <div key={label}>
                    <span>{label}</span>
                    <strong>{value ?? "Not reported"}</strong>
                  </div>
                ))}
              </div>
              <div className="distribution">
                <span className="eyebrow">
                  TOP OBSERVED STATES · ACTION ORDER x0…x5
                </span>
                {rows.map((row) => (
                  <div key={row.bitstring}>
                    <code>{row.bitstring}</code>
                    <span className="distribution-track">
                      <i style={{ width: `${row.probability * 100}%` }} />
                    </span>
                    <span>
                      {row.count} / {(row.probability * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
              {d.optimizer_success === false && (
                <p className="notice">
                  Optimizer did not converge:{" "}
                  {d.optimizer_message ?? "evaluation limit reached"}. Best
                  sampled results are still evaluated independently.
                </p>
              )}
              {d.compiled_qasm2 && (
                <details>
                  <summary>
                    Inspect compiled OpenQASM <span>Real circuit export</span>
                  </summary>
                  <button onClick={copy} className="small-button">
                    {copied ? <Check size={13} /> : <Copy size={13} />}{" "}
                    {copied ? "Copied" : "Copy QASM"}
                  </button>
                  <pre>{d.compiled_qasm2}</pre>
                </details>
              )}
              <p className="fine-print">
                Noiseless simulator · An exponentially constructed six-qubit
                Hamiltonian · No quantum advantage claim.
              </p>
            </>
          )}
        </div>
      )}
    </section>
  );
}
