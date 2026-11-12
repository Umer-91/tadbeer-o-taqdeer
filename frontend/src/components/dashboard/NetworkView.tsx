"use client";
import { useState } from "react";
import type { ActionId, Scenario } from "@/lib/types";

const routes: { id: ActionId; d: string; color: string }[] = [
  { id: "bridge_repair", d: "M166 235 L310 235 L390 235", color: "#48d8f3" },
  {
    id: "temporary_crossing",
    d: "M166 235 L222 295 L390 295 L390 235",
    color: "#48d8f3",
  },
  { id: "hospital_road", d: "M390 235 L455 180 L500 145", color: "#48d8f3" },
  {
    id: "feeder_repair",
    d: "M405 60 L500 145 M405 60 L570 240 L490 340",
    color: "#ffbc61",
  },
  { id: "hospital_solar", d: "M560 110 L500 145", color: "#ffbc61" },
  { id: "pump_generator", d: "M565 370 L490 340", color: "#4a91ff" },
];
const nodes = [
  { id: "village_a", x: 166, y: 235, name: "Village A", type: "Settlement" },
  { id: "village_b", x: 125, y: 358, name: "Village B", type: "Settlement" },
  { id: "village_c", x: 395, y: 405, name: "Village C", type: "Settlement" },
  { id: "hospital", x: 500, y: 145, name: "Hospital", type: "Essential care" },
  {
    id: "pump",
    x: 490,
    y: 340,
    name: "Water pump",
    type: "Safe-water service",
  },
  {
    id: "feeder",
    x: 405,
    y: 60,
    name: "Grid feeder",
    type: "Electricity supply",
  },
];
export default function NetworkView({
  scenario,
  selected,
  comparison = [],
  showPlan,
}: {
  scenario: Scenario;
  selected: ActionId[];
  comparison?: ActionId[];
  showPlan: boolean;
}) {
  const [detail, setDetail] = useState<string | null>(null);
  return (
    <div className="network-view">
      <div className="map-coordinate top">
        SYNTHETIC VALLEY / SCHEMATIC VIEW
      </div>
      <svg
        viewBox="0 0 680 470"
        role="group"
        aria-label={`${scenario.name} infrastructure network. Selected interventions are highlighted.`}
      >
        <defs>
          <pattern
            id="map-grid"
            width="28"
            height="28"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M28 0H0V28"
              fill="none"
              stroke="#ffffff"
              strokeOpacity=".035"
            />
          </pattern>
          <linearGradient id="map-water">
            <stop stopColor="#152c49" />
            <stop offset="1" stopColor="#1c4764" />
          </linearGradient>
        </defs>
        <rect width="680" height="470" fill="url(#map-grid)" />
        {[0, 1, 2, 3, 4].map((n) => (
          <g key={n} opacity={0.12 - n * 0.015} fill="none" stroke="#9b91bd">
            <path
              d={`M${40 + n * 18} 60 Q${130 + n * 15} ${-30 + n * 22} 250 ${80 + n * 18} T${250 + n * 22} 200`}
            />
            <path
              d={`M${25 + n * 18} 70 Q${145 + n * 15} ${-10 + n * 22} 235 ${100 + n * 18} T${225 + n * 22} 205`}
            />
            <path
              d={`M${520 + n * 15} ${240 + n * 10} Q650 ${160 + n * 22} 680 ${300 + n * 18}`}
            />
          </g>
        ))}
        <path
          d="M308-10C252 95 384 133 327 228S275 341 342 480"
          stroke="url(#map-water)"
          strokeWidth="24"
          fill="none"
        />
        <path
          d="M308-10C252 95 384 133 327 228S275 341 342 480"
          stroke="#4a91ff"
          strokeOpacity=".3"
          strokeWidth="1"
          fill="none"
        />
        <path
          d="M166 235 125 358M490 340 395 405"
          stroke="#5b7082"
          strokeWidth="2"
          strokeDasharray="4 7"
          fill="none"
        />
        {routes.map((r) => {
          const enabled = scenario.actions.find((a) => a.id === r.id)?.enabled;
          const active = showPlan && selected.includes(r.id);
          const other = showPlan && comparison.includes(r.id);
          return (
            <g key={r.id}>
              <path
                d={r.d}
                stroke={other ? "#b49aff" : active ? r.color : "#414553"}
                strokeWidth={other ? 9 : active ? 7 : 2}
                strokeOpacity={active || other ? 0.5 : 1}
                fill="none"
              />
              <path
                d={r.d}
                stroke={active ? r.color : enabled ? "#818899" : "#3c3c49"}
                strokeWidth={active ? 2.5 : 1.5}
                strokeDasharray={active ? undefined : "5 6"}
                fill="none"
              />
              <path
                d={r.d}
                stroke="transparent"
                strokeWidth="18"
                fill="none"
                role="button"
                tabIndex={0}
                aria-label={`Inspect ${scenario.actions.find((a) => a.id === r.id)?.label}`}
                onMouseEnter={() => setDetail(r.id)}
                onFocus={() => setDetail(r.id)}
                onClick={() => setDetail(r.id)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    setDetail(r.id);
                  }
                }}
              />
            </g>
          );
        })}
        <g transform="translate(560 110)">
          <rect
            x="-9"
            y="-7"
            width="18"
            height="14"
            rx="1"
            fill="#201e20"
            stroke="#ffbc61"
          />
          <path d="M-3-6V6M3-6V6M-8 0H8" stroke="#ffbc61" strokeWidth=".5" />
        </g>
        <g transform="translate(565 370)">
          <rect
            x="-8"
            y="-8"
            width="16"
            height="16"
            rx="3"
            fill="#182131"
            stroke="#4a91ff"
          />
          <path d="m2-5-5 6h4l-2 4" stroke="#4a91ff" fill="none" />
        </g>
        {nodes.map((n) => (
          <g
            key={n.id}
            className="map-node"
            role="button"
            tabIndex={0}
            aria-label={`Inspect ${n.name}`}
            onClick={() => setDetail(n.id)}
            onFocus={() => setDetail(n.id)}
            onMouseEnter={() => setDetail(n.id)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                setDetail(n.id);
              }
            }}
          >
            <circle cx={n.x} cy={n.y} r="15" fill="#0e121b" stroke="#555768" />
            <circle
              cx={n.x}
              cy={n.y}
              r="4"
              fill={n.id === "hospital" ? "#ddd5ef" : "#9dacc0"}
            />
            <text x={n.x + 22} y={n.y - 3} fill="#c0c3d1" fontSize="11">
              {n.name}
            </text>
            <text
              x={n.x + 22}
              y={n.y + 12}
              fill="#777e91"
              fontSize="8"
              letterSpacing="1"
            >
              {n.type.toUpperCase()}
            </text>
          </g>
        ))}
        <text x="48" y="425" fill="#737b90" fontSize="9" letterSpacing="2">
          N ↑
        </text>
        <path d="M48 438h70m-70-3v6m70-6v6" stroke="#555b6c" />
        <text x="48" y="457" fill="#6b7081" fontSize="8">
          STYLIZED · NOT TO SCALE
        </text>
      </svg>
      <div className="network-inspector" aria-live="polite">
        {detail ? (
          <>
            <b>
              {scenario.actions.find((a) => a.id === detail)?.label ??
                nodes.find((n) => n.id === detail)?.name}
            </b>
            <span>
              {scenario.actions.find((a) => a.id === detail)
                ? `${scenario.actions.find((a) => a.id === detail)?.cost} planning units · ${scenario.actions.find((a) => a.id === detail)?.enabled ? "Intervention available" : "Unavailable in this scenario"}`
                : "Fictional infrastructure · Explore its connected lifelines"}
            </span>
          </>
        ) : (
          <>
            <b>Explore the dependencies</b>
            <span>Hover or focus a node or intervention to inspect.</span>
          </>
        )}
      </div>
    </div>
  );
}
