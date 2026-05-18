import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal, Base, engine
from backend.app.models.team import Team
from backend.app.models.player import Player
from backend.app.models.contract import Contract, ContractYear
from backend.app.models.stats import SeasonalStats

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Create a mock team
    t = Team(team_abbr="TEST", team_nick="Testing", team_color="#000000", team_color2="#FFFFFF")
    db.add(t)
    db.commit()
    
    # 2. Create a mock player with stats and contract
    p = Player(gsis_id="TEST_P1", name="Test Player", position="QB", team_abbr="TEST")
    db.add(p)
    db.commit()
    
    c = Contract(player_id="TEST_P1", team_abbr="TEST", avg_annual=10.0, total_value=20.0)
    db.add(c)
    db.flush()
    
    cy = ContractYear(contract_id=c.id, year=2024, cap_number=10.0, base_salary=8.0, signing_bonus=2.0)
    db.add(cy)
    
    s = SeasonalStats(player_id="TEST_P1", season=2023, total_epa=100.0, games=17)
    db.add(s)
    
    db.commit()
    yield db
    # Cleanup
    Base.metadata.drop_all(bind=engine)

def test_full_analytics_flow(setup_test_db):
    """
    Integration test: Ensure analytics endpoint correctly established replacement level
    and calculates VORP for our mock player.
    """
    response = client.get("/analytics/vorp", params={"team_abbr": "TEST"})
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]['player'] == "Test Player"
    assert data[0]['vorp'] > 0 # Replacement level for 1 player will be lower than their EPA

def test_optimization_api(setup_test_db):
    """
    Integration test: Ensure optimizer suggests a move to clear space.
    """
    # Target 5M savings
    response = client.get("/strategy/optimize/TEST", params={"target": 5.0})
    assert response.status_code == 200
    data = response.json()
    
    assert data["is_target_met"] is True
    assert len(data["suggested_moves"]) > 0
    assert data["suggested_moves"][0]["player"] == "Test Player"

def test_market_inflation_api(setup_test_db):
    """
    Integration test: Market inflation endpoints.
    """
    response = client.get("/market/inflation")
    assert response.status_code == 200
    # Even if 1 player, it should respond without error
    assert isinstance(response.json(), dict)

def test_scenario_persistence(setup_test_db):
    """
    Integration test: Saving and loading a scenario.
    """
    payload = {
        "team_abbr": "TEST",
        "name": "Integration Test Scenario",
        "transactions": [
            {"move_type": "CUT", "player_name": "Test Player", "savings": 8.0, "dead_cap_added": 2.0}
        ]
    }
    
    # Save
    res_save = client.post("/scenarios/", json=payload)
    assert res_save.status_code == 200
    s_id = res_save.json()['id']
    
    # Load
    res_load = client.get("/scenarios/", params={"team_abbr": "TEST"})
    assert res_load.status_code == 200
    scenarios = res_load.json()
    assert any(s['id'] == s_id for s in scenarios)
    
    # Delete
    res_del = client.delete(f"/scenarios/{s_id}")
    assert res_del.status_code == 200

def test_admin_sync_trigger(setup_test_db):
    """
    Integration test: Background sync trigger.
    """
    response = client.post("/admin/sync")
    assert response.status_code == 200
    assert "triggered" in response.json()["message"]
