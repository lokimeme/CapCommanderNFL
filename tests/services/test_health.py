import pytest
from backend.app.services.health import RosterHealthService

def test_resilience_grade_high():
    # Young roster with long contracts and high flexibility
    roster = [
        {"player_id": "P1", "age": 22, "position": "QB", "contract_years": [2024, 2025, 2026, 2027], "max_potential_savings": 5.0},
        {"player_id": "P2", "age": 23, "position": "WR", "contract_years": [2024, 2025, 2026], "max_potential_savings": 3.0},
        {"player_id": "P3", "age": 24, "position": "LT", "contract_years": [2024, 2025, 2026], "max_potential_savings": 4.0},
    ]
    
    res = RosterHealthService.calculate_resilience_grade(roster, 2024)
    
    assert res['grade'] == "A+"
    assert res['resilience_score'] > 90

def test_resilience_grade_low():
    # Old roster with expiring contracts
    roster = [
        {"player_id": "P1", "age": 35, "position": "QB", "contract_years": [2024], "max_potential_savings": 0.0},
        {"player_id": "P2", "age": 33, "position": "WR", "contract_years": [2024], "max_potential_savings": 0.0},
    ]
    
    res = RosterHealthService.calculate_resilience_grade(roster, 2024)
    
    assert res['grade'] in ["C", "D"]
    assert res['resilience_score'] < 50

def test_fragility_points():
    roster = [
        {"player_id": "P1", "name": "Old QB", "age": 35, "position": "QB", "total_epa": 100.0, "years_remaining": 1},
        {"player_id": "P2", "name": "Older QB", "age": 36, "position": "QB", "total_epa": 50.0, "years_remaining": 1},
        {"player_id": "P3", "name": "Rookie QB", "age": 22, "position": "QB", "total_epa": 5.0, "years_remaining": 1},
    ]
    
    fragility = RosterHealthService.identify_roster_fragility_points(roster)
    
    assert len(fragility) > 0
    assert fragility[0]['position'] == "QB"

def test_turnover_prediction():
    roster = [
        {"player_id": "P1", "contract_end_year": 2024, "is_cliff_candidate": False},
        {"player_id": "P2", "contract_end_year": 2026, "is_cliff_candidate": True}, # Cliff candidate
        {"player_id": "P3", "contract_end_year": 2028, "is_cliff_candidate": False},
    ]
    
    turnover = RosterHealthService.predict_roster_turnover(roster, 2025)
    
    # P1 (expires 2024) and P2 (cliff candidate) should count
    assert turnover['predicted_departures'] == 2
    assert turnover['roster_stability'] == "High Volatility"
