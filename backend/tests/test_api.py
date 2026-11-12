import pytest
from fastapi.testclient import TestClient
from raasta.api import app
from raasta.evaluator import evaluate
from raasta.scenarios import get_scenario

client = TestClient(app)

@pytest.mark.parametrize("scenario", ["flood_baseline", "bridge_blocked", "grid_extended_outage"])
@pytest.mark.parametrize("budget", [0, 6, 9, 12])
@pytest.mark.parametrize("algorithm", ["exact", "greedy"])
def test_classical_api(scenario, budget, algorithm):
    response = client.post('/api/optimize', json=dict(scenario_id=scenario, budget=budget, algorithm=algorithm))
    assert response.status_code == 200
    data = response.json()
    expected = evaluate(data['bitstring'], get_scenario(scenario), budget)
    assert expected.feasible
    assert data['utility'] == expected.utility
    assert data['selected_actions'] == list(expected.selected_actions)
    assert all(value == getattr(expected, key) for key, value in data['metrics'].items())

def test_quantum_api():
    response = client.post('/api/optimize', json=dict(scenario_id='flood_baseline', budget=9, algorithm='qaoa', seed=42, shots=512, p=1))
    assert response.status_code == 200
    data = response.json()
    assert sum(row['count'] for row in data['diagnostics']['distribution']) == 512
    assert evaluate(data['bitstring'], get_scenario('flood_baseline'), 9).utility == data['utility']

@pytest.mark.parametrize('change', [dict(budget=-1), dict(budget=13), dict(budget=True), dict(shots=0), dict(p=3), dict(seed=-1), dict(scenario_id='missing'), dict(algorithm='fake')])
def test_invalid(change):
    payload = dict(scenario_id='flood_baseline', budget=9, algorithm='exact')
    assert client.post('/api/optimize', json=payload | change).status_code == 422

def test_health_scenarios_cors():
    assert client.get('/api/health').json()['qiskit_available'] is True
    assert len(client.get('/api/scenarios').json()) == 3
    response = client.options('/api/optimize', headers={'Origin':'http://localhost:3000','Access-Control-Request-Method':'POST'})
    assert response.headers['access-control-allow-origin'] == 'http://localhost:3000'

def test_failure_never_substitutes(monkeypatch):
    def fail(_):
        raise RuntimeError('test failure')
    monkeypatch.setattr('raasta.api.compute', fail)
    response = client.post('/api/optimize', json=dict(scenario_id='flood_baseline', budget=9, algorithm='qaoa'))
    assert response.status_code == 500
    assert 'utility' not in response.json()
