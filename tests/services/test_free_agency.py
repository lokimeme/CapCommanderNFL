import pytest
from backend.app.services.free_agency import FreeAgencyRecommendationEngine

def test_identify_target_fas():
    team_needs = {
        "QB": {"priority": "Critical"},
        "WR": {"priority": "Moderate"},
        "RB": {"priority": "Low"}
    }
    
    available_fas = [
        {"name": "QB Star", "position": "QB", "projected_apy": 40.0, "total_epa": 150.0},
        {"name": "WR Solid", "position": "WR", "projected_apy": 15.0, "total_epa": 60.0},
        {"name": "RB Depth", "position": "RB", "projected_apy": 5.0, "total_epa": 20.0},
    ]
    
    # Large budget
    targets = FreeAgencyRecommendationEngine.identify_target_free_agents(team_needs, available_fas, 100.0)
    
    assert len(targets) == 2 # QB and WR
    assert targets[0]['player'] == "QB Star"

def test_budget_allocation_logic():
    needs = {
        "QB": {"priority": "Critical"},
        "EDGE": {"priority": "Critical"},
        "WR": {"priority": "Moderate"}
    }
    
    # 50M total space
    res = FreeAgencyRecommendationEngine.calculate_budget_allocation(50.0, needs, 40)
    
    # Reserve is 15M, spendable is 35M
    assert res['total_spendable'] == 35.0
    # Critical needs (QB, EDGE) should get 3x more than Moderate (WR)
    # Total units = 3 + 3 + 1 = 7. 35 / 7 = 5M per unit.
    assert res['allocation_by_position']['QB'] == 15.0
    assert res['allocation_by_position']['WR'] == 5.0

def test_market_value_prediction():
    stats = {"position": "WR", "total_epa": 80.0, "age": 27}
    league_avgs = {"WR": 0.5} # 0.5M per EPA
    
    prediction = FreeAgencyRecommendationEngine.predict_market_value(stats, league_avgs)
    
    # 80 * 0.5 = 40.0. Age is fine. 40 * 1.0 (WR premium is 1.0 in code) = 40.0
    # Wait, WR premium is 1.2 in current implementation? Let me check.
    # Ah, in free_agency.py: premiums = {"QB": 1.4, "LT": 1.25, "EDGE": 1.3, "CB": 1.2}
    # WR is not in premiums, so 1.0.
    assert prediction['predicted_apy'] == 40.0
    
    # Test age penalty
    old_stats = {"position": "WR", "total_epa": 80.0, "age": 32}
    old_pred = FreeAgencyRecommendationEngine.predict_market_value(old_stats, league_avgs)
    assert old_pred['predicted_apy'] < 40.0
