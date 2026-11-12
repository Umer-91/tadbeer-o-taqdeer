"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  Cell,
} from "recharts";
import type { Algorithm, SolverResult } from "@/lib/types";
export default function AlgorithmComparison({
  results,
}: {
  results: Partial<Record<Algorithm, SolverResult>>;
}) {
  const data = (["qaoa", "exact", "greedy"] as const).flatMap((id) =>
    results[id]?.status === "ok"
      ? [
          {
            algorithm:
              id === "qaoa" ? "QAOA" : id === "exact" ? "Exact" : "Greedy",
            utility: results[id]!.utility,
            color:
              id === "qaoa"
                ? "#a18af4"
                : id === "exact"
                  ? "#48d8f3"
                  : "#7c879c",
          },
        ]
      : [],
  );
  return (
    <div className="comparison-chart">
      <div className="panel-heading">
        <h3>Algorithm comparison</h3>
        <span>SERVICE SCORE</span>
      </div>
      {data.length ? (
        <>
          <div
            role="img"
            aria-label={data
              .map((d) => `${d.algorithm}: ${d.utility}`)
              .join(", ")}
          >
            <ResponsiveContainer width="100%" height={145}>
              <BarChart
                data={data}
                layout="vertical"
                margin={{ left: 0, right: 25, top: 10, bottom: 0 }}
              >
                <XAxis type="number" hide />
                <YAxis
                  type="category"
                  dataKey="algorithm"
                  width={48}
                  tick={{ fill: "#a2a7b8", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  cursor={{ fill: "#ffffff06" }}
                  contentStyle={{
                    background: "#151722",
                    border: "1px solid #383543",
                    fontSize: 12,
                  }}
                />
                <Bar
                  dataKey="utility"
                  barSize={13}
                  radius={[0, 2, 2, 0]}
                  isAnimationActive={false}
                >
                  {data.map((row) => (
                    <Cell key={row.algorithm} fill={row.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="fine-print">
            Only completed runs for the current scenario and budget.{" "}
            {data.length < 3
              ? "Run other algorithms to compare."
              : "Higher service score is better."}
          </p>
        </>
      ) : (
        <div className="empty-chart">
          <span />
          <span />
          <span />
          <p>Run an algorithm to begin comparison.</p>
        </div>
      )}
    </div>
  );
}
