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

def test_timeout_retains_capacity_until_worker_finishes(monkeypatch):
    import asyncio
    import threading
    from raasta import api
    entered = threading.Event()
    finish = threading.Event()
    capacity = threading.BoundedSemaphore(1)
    monkeypatch.setattr(api, '_capacity', capacity)
    monkeypatch.setattr(api, 'COMPUTE_TIMEOUT_SECONDS', 0.02)
    def slow(_):
        entered.set()
        finish.wait(2)
        return {}
    monkeypatch.setattr(api, 'compute', slow)
    request = api.OptimizeRequest(scenario_id='flood_baseline', budget=9, algorithm='exact')
    async def exercise():
        try:
            with pytest.raises(api.HTTPException) as timeout:
                await api.optimize(request)
            assert entered.is_set() and timeout.value.status_code == 504
            with pytest.raises(api.HTTPException) as busy:
                await api.optimize(request)
            assert busy.value.status_code == 503
        finally:
            finish.set()
    asyncio.run(exercise())
    assert capacity.acquire(blocking=False)
    capacity.release()

def test_missing_quantum_returns_503(monkeypatch):
    from raasta import api
    def unavailable(_):
        raise ImportError('test unavailable')
    monkeypatch.setattr(api.importlib, 'import_module', unavailable)
    response = client.post('/api/optimize', json=dict(scenario_id='flood_baseline', budget=9, algorithm='qaoa'))
    assert response.status_code == 503
    assert 'utility' not in response.json()

def test_no_feasible_sample_preserves_empty_result(monkeypatch):
    from raasta.quantum import result_from_counts
    result = result_from_counts({'111111': 8}, get_scenario('flood_baseline'), 9, {'runtime_ms': 1, 'shots': 8, 'exact_optimum': 96})
    monkeypatch.setattr('raasta.api.compute', lambda _: result.to_dict())
    response = client.post('/api/optimize', json=dict(scenario_id='flood_baseline', budget=9, algorithm='qaoa'))
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'no_feasible_sample'
    assert data['bitstring'] is None and data['utility'] is None
    assert data['selected_actions'] == []
