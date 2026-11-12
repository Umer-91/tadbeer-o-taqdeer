export const ACTION_IDS = [
  "bridge_repair",
  "temporary_crossing",
  "hospital_road",
  "feeder_repair",
  "hospital_solar",
  "pump_generator",
] as const;
export type ActionId = (typeof ACTION_IDS)[number];
export type Algorithm = "qaoa" | "exact" | "greedy";
export interface Action {
  id: ActionId;
  index: number;
  label: string;
  cost: number;
  enabled: boolean;
}
export interface ScenarioNode {
  id: string;
  label: string;
  kind: string;
  population?: number | null;
  priority_weight?: number | null;
}
export interface ScenarioLink {
  id: string;
  source: string;
  target: string;
  lifeline: "road" | "electricity" | "water";
  action_ids: ActionId[];
  currently_working?: boolean;
}
export interface Scenario {
  id: string;
  name: string;
  description: string;
  budget_default: number;
  actions: Action[];
  nodes: ScenarioNode[];
  links: ScenarioLink[];
  synthetic: true;
}
export interface OptimizeRequest {
  scenario_id: string;
  budget: number;
  algorithm: Algorithm;
  seed?: number;
  shots?: number;
  p?: number;
}
export interface Metrics {
  hospital_operational: boolean;
  water_operational: boolean;
  basic_connectivity: boolean;
  hospital_power: boolean;
}
export interface DistributionEntry {
  bitstring: string;
  probability: number;
  count: number;
}
export interface Diagnostics {
  runtime_ms: number;
  shots?: number;
  depth?: number;
  gate_count?: number;
  feasible_sample_rate?: number;
  distribution?: DistributionEntry[];
  optimizer_evaluations?: number;
  exact_optimum?: number;
  optimality_gap?: number | null;
  compiled_qasm2?: string;
  logical_circuit?: string;
  optimizer_success?: boolean;
  optimizer_message?: string;
  seed?: number;
  p?: number;
}
export interface SolverResult {
  scenario_id: string;
  algorithm: Algorithm;
  budget: number;
  status: "ok" | "no_feasible_sample" | "error";
  selected_actions: ActionId[];
  bitstring: string | null;
  feasible: boolean | null;
  utility: number | null;
  total_cost: number | null;
  metrics: Metrics | null;
  diagnostics: Diagnostics;
  warnings: string[];
}
