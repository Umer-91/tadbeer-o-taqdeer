import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'experiments/results/benchmark-phase3-seed42.json').read_text(encoding='utf8'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)
def diagram(name, labels):
 im=Image.new('RGB',(1500,800),'white'); draw=ImageDraw.Draw(im)
 for i,label in enumerate(labels):
  y=30+i*145; draw.rounded_rectangle((100,y,1400,y+105),radius=12,fill='#eeeaf8',outline='#615080',width=3);draw.multiline_text((140,y+20),label,font=font,fill='#151020',spacing=8)
  if i<len(labels)-1: draw.line((750,y+105,750,y+145),fill='#615080',width=4);draw.polygon([(740,y+135),(760,y+135),(750,y+145)],fill='#615080')
 im.save(root/'docs'/name)
diagram('architecture.png',['Browser: Next.js + R3F story and dashboard','HTTP typed JSON / FastAPI validation / explicit localhost CORS','Synthetic scenarios + authoritative constraint and service evaluator','Qiskit QAOA simulator | Exact 64-state enumeration | Greedy','Validated result JSON -> selected links, service metrics, charts and evidence'])
diagram('dependencies.png',['Crossing = bridge repair OR temporary crossing','Hospital access = crossing AND hospital road','Hospital service = hospital access AND (feeder OR solar)','Water service = crossing AND (feeder OR pump generator)','Stylized dependencies only / synthetic data / no infrastructure control'])
doc=Document();sec=doc.sections[0];sec.top_margin=sec.bottom_margin=Inches(.7)
for name in ['Normal','Title','Heading 1','Heading 2']:
 st=doc.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
doc.styles['Normal'].font.size=Pt(11)
def p(t):doc.add_paragraph(t)
def h(t):doc.add_heading(t,1)
def page():doc.add_page_break()
doc.add_heading('Tadbeer o Taqdeer disaster recovery optimization',0)
p('Qiskit Fall Fest 2026 | Disaster Response | 12 November 2026')
p('Team and institution: TODO supplied by project owner')
h('Abstract')
p('Tadbeer-o-Taqdeer models restoration choices across roads, electricity and water in a fictional Pakistan-inspired valley. A six-qubit QAOA circuit samples candidate portfolios, while exhaustive enumeration independently establishes the optimum. Nine fixed-seed simulator experiments reached the exact optimum in their best feasible sample. All optimizations reached their evaluation cap without convergence; these observations do not establish quantum advantage.')
h('Motivation and scope')
p('Floods and landslides can interrupt several lifelines together. Repairing an individual asset may provide little service unless its dependencies are also available. This prototype makes that coupling visible to judges and researchers. It uses synthetic infrastructure, abstract planning units and illustrative service weights; it is not a dispatch system or a model of an actual Pakistani district.')
p('The interface preserves the Urdu identity as selectable Nastaliq text, with English controls for international reviewers. The cinematic scene is explicitly illustrative; only backend responses supply restoration results.')
page();h('Model and constraints')
t=doc.add_table(rows=1, cols=3);t.style='Light Shading Accent 1'
for c,v in zip(t.rows[0].cells,['Variable','Intervention','Cost']):c.text=v
for i,label,cost in [(0,'Main bridge repair',4),(1,'Temporary crossing',2),(2,'Hospital access road',2),(3,'Electricity feeder repair',4),(4,'Hospital solar backup',3),(5,'Pump generator',2)]:
 for c,v in zip(t.add_row().cells,[f'x{i}',label,str(cost)]):c.text=v
p('Each xi is binary. Budget defaults to 9 and the API accepts 0 through 12. Total cost must not exceed budget. Disabled actions cannot be selected. Bridge repair and temporary crossing are alternatives: x0 + x1 <= 1.')
p('U = 50 hospital_operational + 30 water_operational + 15 basic_connectivity + 5 hospital_power - 0.5 total_cost. Utility is an abstract weighted service score, not people saved. Fixed weights are design assumptions, not fitted evidence.')
doc.add_picture(str(root/'docs/dependencies.png'),width=Inches(6.2))
page();h('Quantum method and baselines')
p('A canonical bitstring lists x0 through x5. Qiskit measurement strings use reverse display ordering; conversion is tested against every computational basis state. The six-qubit diagonal Hamiltonian is built from the evaluator over all 64 choices. Its energy is negative utility plus a penalty for budget overflow, disabled choices and exclusivity. The penalty bound and fractional-budget handling are documented in docs/MODEL.md and tested exhaustively.')
p('The circuit starts in a uniform superposition, applies a diagonal phase separator and RX mixers. Default p = 1, seed = 42, with COBYLA bounded to 60 objective evaluations. Training uses exact statevector expectations; final counts come from 512 actual Qiskit Aer shots. Compiled OpenQASM, parameters, optimizer trace, depth and gate counts are saved with results. p = 2 is supported but is not part of this nine-case benchmark.')
p('Exact enumeration ranks all feasible choices by maximum utility, then minimum cost, then lexicographic bitstring. Greedy repeatedly chooses a feasible action with the highest positive marginal utility per cost, using stable ties. Its myopic rule may miss complementary interventions. The returned quantum plan is the best feasible observed sample, not a guaranteed optimum; a no-feasible-sample response contains no replacement solution.')
h('Scientific limitations')
p('Truth-table Hamiltonian construction and statevector simulation scale exponentially. These are noiseless CPU simulations, not hardware measurements. A single seed per case is not a statistical study. The optimizer did not converge within the evaluation cap. There is no runtime or quantum advantage claim. Infrastructure dependencies omit hydraulic and electrical physics and real repair logistics.')
page();h('Measured results')
p('Source: experiments/results/benchmark-phase3-seed42.json. Executed '+d['environment']['timestamp_utc']+'. Each row uses p=1, seed 42 and 512 final shots. No seed search was performed.')
t=doc.add_table(rows=1,cols=6);t.style='Light Shading Accent 1'
for c,v in zip(t.rows[0].cells,['Scenario','Budget','Exact U','Greedy U','QAOA U','Feasible %']):c.text=v
for r in d['runs']:
 vals=[r['scenario']['id'],r['budget'],r['exact']['utility'],r['greedy']['utility'],r['qaoa']['utility'],round(100*r['qaoa']['diagnostics']['feasible_sample_rate'],2)]
 for c,v in zip(t.add_row().cells,vals):c.text=str(v)
p('All nine best sampled feasible QAOA utilities match exact in these recorded runs. Feasible-sample rates vary; best-sample optimality must not be interpreted as optimizer convergence or a future guarantee. All 27 solver records were independently verified against the evaluator and recorded source hashes.')
h('Environment and validation')
p('Python '+d['environment']['python']+' on Windows 11 AMD64; '+str(d['environment']['packages'])+'. CPU: '+d['environment']['processor']+'. Backend validation: 121 tests passed, including genuine QAOA over the API. Frontend lint, type checking and production build passed. Local API health and frontend HTTP checks succeeded. Live browser verification of the integrated version remains pending because browser access was unavailable in this chat.')
page();h('Application architecture')
doc.add_picture(str(root/'docs/architecture.png'),width=Inches(6.2))
p('FastAPI exposes /api/health, /api/scenarios and /api/optimize, with interactive documentation at /docs. Request validation bounds budget, shots, seed and layers. A 25-second HTTP timeout returns an explicit error; a running worker may finish its bounded 60 evaluations after cancellation. This local prototype is not hardened for public multi-user hosting.')
p('The frontend fetches live scenarios and posts the selected algorithm and parameters. Scores and network highlights come from the returned result. Failed computation is never relabeled as an exact success. Comparison requires distinct successful Exact and QAOA requests.')
doc.add_picture(str(root/'docs/assets/phase-2/dashboard-1440x900.jpg'),width=Inches(6.2))
p('Figure: actual Phase 2 design-preview screenshot, not a screenshot of a live computed Phase 3 result. Integrated browser capture remains pending.')
page();h('Reproduction and references')
p('Create Python 3.12 virtual environment; install backend/requirements.lock.txt and the editable backend package. Run python -m pytest -q backend/tests. Start python -m uvicorn raasta.api:app --host 127.0.0.1 --port 8000. In frontend run npm ci, npm run build and npm run start using Node 24. Set NEXT_PUBLIC_API_BASE_URL if the local API address changes.')
p('Reproduce experiments with python experiments/run_benchmarks.py --seed 42 --shots 512 --output experiments/results/new-run.json, then python experiments/verify_results.py experiments/results/new-run.json. Never overwrite the measured source file for this report.')
p('Primary implementation references: Qiskit documentation https://quantum.cloud.ibm.com/docs/ ; Qiskit Aer https://qiskit.github.io/qiskit-aer/ ; FastAPI https://fastapi.tiangolo.com/ ; Next.js https://nextjs.org/docs . Exact API usage is captured by installed versions and repository tests.')
p('Credits: original procedural terrain and network graphics. Noto Nastaliq Urdu and Manrope use SIL OFL licenses distributed in frontend/public/licenses. GSAP uses its standard license. No AI-generated Urdu imagery is used.')
h('Next research steps')
p('Validate weights with domain specialists; introduce uncertainty, repair durations and larger dependency graphs; compare against stronger classical heuristics; report multiple seeds and noise sensitivity. Scaling requires a different Hamiltonian construction. Operational use would require real data, safety review and expert validation.')
doc.save(root/'docs/report.docx')
print('Created docs/report.docx and two architecture diagrams')
