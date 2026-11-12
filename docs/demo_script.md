# Three minute demonstration

Rehearse to 180 seconds. Keep the app running in two terminals and preflight API health. Use flood_baseline, budget 9, seed 42, p=1, shots 512. Record real runs; do not imply a saved run is live.

| Time | Onscreen action and spoken message |
|---|---|
| 0:00–0:25 | Show Urdu hero and valley. “Tadbeer-o-Taqdeer means strategy and destiny. After a flood, damaged roads, electricity and water can fail together. This fictional Pakistan-inspired valley asks which repairs restore the most service with limited resources.” |
| 0:25–0:50 | Scroll through the dependency story. “A bridge alone does not operate a hospital. The hospital needs access and power. Water restoration also requires crossing access and pump power. We evaluate these connections jointly.” |
| 0:50–1:20 | Enter command center; show budget 9 and six actions. “We choose six binary interventions under a budget and mutually exclusive crossing alternatives. Our score combines hospital, water, connectivity and power benefits, minus cost. These are synthetic planning units and service weights, not people saved.” |
| 1:20–2:15 | Run QAOA, then Exact, then Greedy. Return to QAOA and expand evidence. “This runs an actual six-qubit Qiskit circuit. Here are the measured counts and feasible-sample rate. Exact checks all 64 choices; greedy follows marginal benefit per cost. The recorded default experiment found utility 96 versus greedy 95.5. The optimizer reached its evaluation cap, so a best sampled optimum does not mean convergence.” Show actual values if a new run differs. |
| 2:15–2:40 | Select bridge unavailable; run Exact, inspect temporary crossing, toggle Before/Selected plan. “Changing available interventions changes the feasible restoration portfolio. The diagram highlights only interventions returned by the computation.” |
| 2:40–3:00 | Return to evidence or architecture. “This is a small noiseless simulation with exponentially constructed energies, not evidence of quantum advantage. Our contribution is a reproducible, inspectable demonstration of coupled recovery choices. Where Strategy Shapes Destiny.” |

If the backend fails, show the error honestly. Open the committed benchmark JSON and say “This is a recorded local simulator run,” identifying seed, shots and timestamp. Do not stage a fabricated live success. User records/uploads the video, verifies duration <=180 seconds and tests anonymous link access.
