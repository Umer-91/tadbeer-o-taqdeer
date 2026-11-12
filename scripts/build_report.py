"""Build the final report from recorded experiments; never run a solver here."""
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'experiments/results/benchmark-phase3-seed42.json').read_text(encoding='utf-8'))
doc = Document()
s = doc.sections[0]
s.page_width, s.page_height = Inches(8.27), Inches(11.69)
s.top_margin = s.bottom_margin = Inches(.65)
s.left_margin = s.right_margin = Inches(.75)
for name in ('Normal','Title','Heading 1','Heading 2'):
    doc.styles[name].font.name = 'Calibri'
    doc.styles[name].font.color.rgb = RGBColor(0,0,0)
doc.styles['Normal'].font.size = Pt(11)
doc.styles['Normal'].paragraph_format.space_after = Pt(7)
doc.styles['Normal'].paragraph_format.line_spacing = 1.05
doc.styles['Title'].font.size = Pt(28)
doc.styles['Heading 1'].font.size = Pt(18)
doc.styles['Heading 2'].font.size = Pt(13)
def p(text): return doc.add_paragraph(text)
def h(text): doc.add_heading(text,1)
def sub(text): doc.add_heading(text,2)
def page(): doc.add_page_break()
def table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers)); t.autofit = False
    t.style = 'Table Grid'
    for cell, text in zip(t.rows[0].cells, headers):
        cell.text = text
        sh = OxmlElement('w:shd'); sh.set(qn('w:fill'),'393246'); cell._tc.get_or_add_tcPr().append(sh)
        for run in cell.paragraphs[0].runs: run.bold=True; run.font.color.rgb=RGBColor(255,255,255)
    for i,row in enumerate(rows):
        cells=t.add_row().cells
        for cell,text in zip(cells,row):
            cell.text=str(text)
            if i%2==0:
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'F3F1F5');cell._tc.get_or_add_tcPr().append(sh)
    for row in t.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                para.paragraph_format.space_after=Pt(5);para.paragraph_format.space_before=Pt(5)
                for run in para.runs:run.font.size=Pt(10)
    return t

doc.add_heading('Tadbeer-o-Taqdeer',0)
p('Disaster recovery optimization with Qiskit')
p('Where Strategy Shapes Destiny.')
p('Umer Asif | Ali Irtiza | Abdullah Khalil\nFAST-NUCES Islamabad\nQiskit Fall Fest 2026 | Disaster Response\n12 November 2026')
h('Why we chose this problem')
p('We are students from Pakistan. Floods can leave rural communities without safe crossings, hospital access, electricity or water. When resources are limited, every repair cannot happen at once. We wanted to explore a simple question: which combination of repairs restores the most important services within a fixed budget?')
p('Choosing the cheapest repair first is one possible simple strategy. We do not claim that this is how Pakistan’s government makes decisions. Our interest is in the connections between repairs. A repaired hospital road is useful, but hospital care also needs power. A combination can achieve more than separate choices suggest.')
h('What we built')
p('Tadbeer-o-Taqdeer is a small research prototype with a fictional Pakistan-inspired valley. It compares Qiskit QAOA, a quantum optimization method, with two classical methods called Exact and Greedy. An interactive website lets a visitor change the disaster scenario and budget, run a method, and inspect the returned repairs and service score.')
p('We chose Disaster Response because restoring essential services after damage is the central question. Electricity and water are connected parts of that question. The prototype is intended for learning and exploring planning ideas; it does not make emergency decisions or control infrastructure.')
h('What the results show')
p('For the synthetic flood at budget 9, the best observed QAOA plan scored 96, matching Exact. Greedy scored 95.5. QAOA used a simulator, not a physical quantum computer. This result demonstrates a working experiment, not a quantum speedup or a guarantee of better future results.')
page();h('The six repair decisions')
p('Each action has a fixed fictional cost in planning units. These are not rupees or estimates for real construction. All three scenarios use the costs below.')
table(['Choice','Action and purpose','Cost'],[
('x0','Repair main bridge: restore a crossing',4),('x1','Establish temporary crossing: an alternative route',2),('x2','Repair hospital access road: connect the hospital route',2),('x3','Repair electricity feeder: supply hospital and pump power',4),('x4','Install hospital solar-battery backup: local hospital power',3),('x5','Deploy pump generator: local water-pump power',2)])
sub('How a plan is written')
p('A bit is a 0 or 1. Here 0 means leave an action out and 1 means select it. Six choices give 2 × 2 × 2 × 2 × 2 × 2 = 64 combinations. We write them in action order x0 through x5. For example, 011100 selects x1, x2 and x3: a temporary crossing, hospital road and electricity feeder.')
sub('What makes a plan allowed')
p('The total cost must fit the chosen budget. The main bridge and temporary crossing are alternatives, so a plan cannot select both. An action disabled by the scenario must stay at 0. The empty plan is allowed. The website accepts budgets from 0 to 12; the default is 9.')
sub('Three fictional situations')
p('Synthetic valley flood: all six actions are available. Bridge unavailable: x0 cannot be repaired, but x1 remains available. Extended grid outage: x3 is unavailable, so local power alternatives matter. These are synthetic examples, not reports from real villages.')
sub('Why repairs depend on each other')
p('Either crossing provides basic connectivity. Hospital access needs a crossing and the hospital road. Hospital care then needs access and power from the feeder or solar backup. Water service needs a crossing and pump power from the feeder or generator. We assume crews need crossing access to restore water. These are simple rules, not detailed electrical or water-flow models.')
page();h('Scoring a repair plan')
p('Utility means the model’s weighted service score. A service that works contributes its weight; a service that does not work contributes zero. The weights are our explicit design assumptions. They do not represent people saved, real population benefits or measured medical outcomes.')
table(['Reward or deduction','Score'],[('Hospital operational',50),('Water operational',30),('Basic crossing connectivity',15),('Hospital power',5),('Cost deduction','Subtract 0.5 × total cost')])
p('U = 50 × hospital + 30 × water + 15 × connectivity + 5 × hospital power − 0.5 × cost. Each service indicator is 0 or 1. Hospital power is rewarded separately even when full hospital service is not restored. Hard constraints still apply: a high score cannot make an invalid plan acceptable.')
sub('Worked example with budget 9')
p('1. Choose 011100: temporary crossing, hospital access road and electricity feeder.\n2. Add the costs: 2 + 2 + 4 = 8. This fits budget 9, selects one crossing and uses enabled actions in the flood scenario.\n3. The crossing and road provide hospital access. The feeder provides hospital and pump power. All four rewarded services therefore work.\n4. Add rewards: 50 + 30 + 15 + 5 = 100.\n5. Subtract the cost deduction: 0.5 × 8 = 4. Final utility: 100 − 4 = 96.')
p('The recorded Greedy plan is 011011: temporary crossing, hospital road, solar backup and pump generator. Its cost is 2 + 2 + 3 + 2 = 9. It restores the same rewarded services, so its score is 100 − 4.5 = 95.5. The 0.5 difference comes from the extra planning unit, not from a claim about additional lives saved.')
sub('The two classical comparisons')
p('Exact checks every one of the 64 combinations, rejects invalid ones and keeps the highest utility. It gives the reference optimum for this small model. Ties prefer lower cost, then the alphabetically earlier bitstring.')
p('Greedy starts with nothing selected. It repeatedly adds the allowed action with the largest positive score increase per added cost. It stops when no positive addition is possible. This one-step view can miss repairs that are useful together. It is a simple comparison, not a description of government practice.')
page();h('What quantum means in this project')
p('A qubit is the quantum counterpart of a bit. Before measurement, its state can contain amplitudes for 0 and 1; this is called superposition. Amplitudes determine measurement probabilities. Measurement gives an ordinary bitstring, not a list of all answers. A quantum circuit is a sequence of operations, called gates, that changes those amplitudes.')
p('Qiskit is the software toolkit we use to build and execute the circuit. QAOA stands for Quantum Approximate Optimization Algorithm. It combines a quantum circuit with a classical adjustment loop. It is relevant here because selecting a repair combination is a discrete optimization problem. For only six decisions, Exact is already practical and much faster in our recorded example.')
sub('How our actual implementation works')
p('1. Map each action to one qubit. The evaluator calculates utility and rule violations for all 64 plans. A Hamiltonian is the energy rule given to the circuit. We use E = −U + P × violations, so lower energy favors useful, valid plans.')
p('2. Violations add budget overflow, selecting both crossings, and selected disabled actions. Let Δ be the smallest positive violation and R the utility range over all plans. The code sets P = (R + 1) / min(1, Δ). This makes the minimum invalid-plan penalty exceed R, including fractional budgets. A check confirms that an invalid plan cannot become the lowest-energy answer.')
p('3. Prepare all six qubits in a uniform superposition. A cost layer changes phases according to scaled energy. A mixing layer uses RX rotations to change the probabilities. Phase is part of a quantum amplitude; its interference with other amplitudes can change which plans are measured. One pair of layers is p = 1, used in the benchmarks.')
p('4. COBYLA, a classical numerical optimizer, adjusts the circuit angles to lower average energy. The training calculation uses Qiskit’s exact statevector simulation, which tracks all amplitudes. It does not use measurement shots during training. The saved runs use seed 42 and a cap of 60 evaluations.')
p('5. Qiskit compiles the circuit into one- and two-qubit gates. Aer, Qiskit’s simulator, then takes 512 shots. A shot is one sampled measurement. The code reverses Qiskit’s displayed bit order into x0 through x5, evaluates each observed plan and returns the best feasible observed plan. It never replaces a failed QAOA sample with Exact.')
p('This is genuine execution of a Qiskit circuit on a noiseless simulator. Constructing its energy table already enumerates 64 states, so the method scales exponentially. It is a small demonstration of the method, not an efficient solution for large networks.')
page();h('Recorded experimental results')
p('Source: experiments/results/benchmark-phase3-seed42.json. Recorded on 12 November 2026 at 14:00:50 UTC. Every case uses six qubits, seed 42, p = 1, 512 final shots and at most 60 optimizer evaluations. These saved experiments were not rerun to write this report.')
labels={'flood_baseline':'Flood','bridge_blocked':'Bridge unavailable','grid_extended_outage':'Grid outage'}
rows=[]
for r in data['runs']:
    rows.append([labels[r['scenario']['id']],r['budget'],f"{r['exact']['utility']:g}",f"{r['greedy']['utility']:g}",f"{r['qaoa']['utility']:g}",f"{100*r['qaoa']['diagnostics']['feasible_sample_rate']:.2f}%"])
table(['Scenario','Budget','Exact','Greedy','QAOA best','Feasible shots'],rows)
p('Scores are utility units; higher is better. “Feasible shots” is the share of measurements that satisfy all constraints, not the chance of measuring the optimum. QAOA best means the best feasible observed sample among the 512 shots.')
sub('The flood example at budget 9')
r=next(r for r in data['runs'] if r['scenario']['id']=='flood_baseline' and r['budget']==9)
q=r['qaoa']['diagnostics']
p(f"QAOA returned 011100 with cost 8 and utility 96. There were 448 feasible samples out of 512 (87.5%). The compiled circuit had depth {q['depth']} and {q['gate_count']} gates. Depth counts sequential circuit layers; gates count operations, excluding measurements and barriers here.")
p('Recorded solver times were QAOA {:.1f} ms, Exact {:.3f} ms and Greedy {:.3f} ms. These are single local measurements, not a speed comparison study or a live-demo timing guarantee.'.format(q['runtime_ms'],r['exact']['diagnostics']['runtime_ms'],r['greedy']['diagnostics']['runtime_ms']))
p('All nine best observed QAOA scores matched Exact in these saved runs. However, all nine optimizers reached the evaluation cap without reporting convergence. Finding a good sampled plan does not mean the adjustment process settled, or that a different run will do equally well. There is no demonstrated quantum advantage.')
sub('Recorded environment')
p('Python '+data['environment']['python']+'. Package versions: '+', '.join(f'{k} {v}' for k,v in data['environment']['packages'].items())+'. Full environment details, counts, circuit export and optimizer traces are in the JSON file.')
page();h('How the application fits together')
doc.add_picture(str(ROOT/'docs/architecture.png'),width=Inches(6.1))
p('The visitor chooses a scenario, budget and algorithm, then clicks Run Optimization. The Next.js website sends a JSON request to FastAPI, the Python web server. FastAPI validates inputs and calls the real solver. The evaluator checks the plan. The response supplies the selected repairs, service score and diagnostics used by the website.')
doc.add_picture(str(ROOT/'docs/dependencies.png'),width=Inches(6.1))
p('The dependency diagram lists service rules, not the order repairs must be performed. “OR” means either option is enough; “AND” means both are needed. Feeder repair can power both the hospital and the pump, explaining why connected choices can matter.')
page();h('Using and reproducing the prototype')
p('The website presents a stylized mountain valley, selectable Urdu Nastaliq branding and English controls. Scenario and budget controls change the optimization request. Algorithm controls choose QAOA, Exact or Greedy. Run each method for the same inputs to compare scores. The quantum evidence panel shows the QAOA circuit and measurement distribution, even when another method is currently selected.')
p('A computed result comes from a successful backend response. A preview, cinematic scene or saved benchmark is not a new computation. Connection failures and solver failures must remain visible. The dashboard does not silently substitute recorded answers when the backend is unavailable.')
sub('Run on Windows')
p('Use Python 3.12 or newer and Node.js 22 or newer (the recorded development environment used Python 3.12.10 and Node 24). From the repository root, create a virtual environment if needed:')
for line in [r'py -3.12 -m venv .venv',r'.\.venv\Scripts\python.exe -m pip install -r backend/requirements.lock.txt',r'.\.venv\Scripts\python.exe -m pip install --no-deps --no-build-isolation -e backend',r'.\.venv\Scripts\python.exe -m uvicorn raasta.api:app --host 127.0.0.1 --port 8000']:
    p(line)
p('In a second terminal, enter frontend, run npm ci, then npm run build and npm run start. Open http://127.0.0.1:3000. API documentation is at http://127.0.0.1:8000/docs. The root README has copyable commands and the existing-machine Node fallback.')
sub('Check and reproduce')
p(r'Run .\.venv\Scripts\python.exe -m pytest -q backend/tests for backend validation. In frontend, npm test checks the API client. Tests cover model rules, energy mapping, bit order, solver results and API behavior.')
p(r'To deliberately repeat the experiments, run .\.venv\Scripts\python.exe experiments/run_benchmarks.py --seed 42 --shots 512 --maxiter 60 --output experiments/results/my-new-run.json. Then run .\.venv\Scripts\python.exe experiments/verify_results.py experiments/results/my-new-run.json. Always choose a new filename; do not overwrite the saved evidence.')
sub('Reproducible evidence')
p('Recorded files include environment versions and source hashes. Exact supplies an independent reference optimum. Re-evaluating saved bitstrings checks their costs, constraints and utility without rerunning QAOA. The repository retains tests and locked dependencies so another developer can inspect the assumptions and repeat the work.')
page();h('Limitations and next steps')
p('The valley, action costs and weights are fictional. Planning units are abstract. There are only six decisions, with simplified dependencies and no repair durations, uncertainty, crew routing, hydraulic simulation or electrical power-flow simulation. Population metadata does not enter the utility formula.')
p('The quantum computation runs on a noiseless simulator, not physical quantum hardware. Only one seed and one optimizer start were used for each case. Every recorded optimizer hit the evaluation cap without convergence. The best observed sample is not a guarantee of typical performance.')
p('The Hamiltonian construction enumerates every plan, and statevector simulation also scales exponentially. The classical Exact method already solves this instance quickly. We have not demonstrated quantum speedup or superiority over strong classical optimization methods. This local prototype is not ready for real emergency decisions or public operational deployment.')
h('References and credits')
p('Project evidence: docs/MODEL.md; backend/raasta/evaluator.py, energy.py, quantum.py, exact.py and greedy.py; experiments/results/benchmark-phase3-seed42.json. These define the model and recorded results.')
p('Qiskit documentation: https://quantum.cloud.ibm.com/docs/\nQiskit Aer documentation: https://qiskit.github.io/qiskit-aer/\nFarhi, Goldstone and Gutmann, A Quantum Approximate Optimization Algorithm (2014): https://arxiv.org/abs/1411.4028\nFastAPI: https://fastapi.tiangolo.com/\nNext.js: https://nextjs.org/docs')
p('The terrain and network visualization are procedural illustrations. Noto Nastaliq Urdu and Manrope font licenses are included in frontend/public/licenses. The frontend uses Three.js, React Three Fiber, GSAP and Recharts; package versions are recorded in its lockfile. Urdu branding is real selectable text, not an AI-generated image.')
h('Conclusion')
p('We built a working way to explore connected flood-recovery choices and compare a genuine Qiskit QAOA experiment with classical answers. The main lesson is that combinations matter: restoring access and power together can unlock a useful service. Our recorded small-instance results are encouraging as a learning demonstration, with clear limits.')
p('A real planning system would need verified local data, repair-time and uncertainty models, input from disaster-response and infrastructure specialists, stronger classical comparisons and repeated experiments. Larger quantum studies would also need a scalable formulation and noise analysis. Any operational use would require expert validation and safety review.')
doc.core_properties.author='Umer Asif; Ali Irtiza; Abdullah Khalil'
doc.core_properties.title='Tadbeer-o-Taqdeer disaster recovery optimization'
doc.save(ROOT/'docs/report.docx')
print('Updated docs/report.docx from nine recorded cases; both existing diagrams embedded.')
