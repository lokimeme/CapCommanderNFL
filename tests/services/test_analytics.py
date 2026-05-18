import pytest
from backend.app.services.analytics import AdvancedMetricsEngine

def test_replacement_level_calculation():
    # Mock player data for a single position
    players = [
        {"position": "QB", "total_epa": 100.0},
        {"position": "QB", "total_epa": 80.0},
        {"position": "QB", "total_epa": 60.0},
        {"position": "QB", "total_epa": 40.0},
        {"position": "QB", "total_epa": 20.0},
        {"position": "QB", "total_epa": 10.0},
        {"position": "QB", "total_epa": 5.0},
        {"position": "QB", "total_epa": 2.0},
        {"position": "QB", "total_epa": 1.0},
        {"position": "QB", "total_epa": 0.0},
    ]
    
    levels = AdvancedMetricsEngine.calculate_positional_replacement_level(players)
    
    # n=10. 60th to 80th percentile is index 6 and 7 (5.0 and 2.0)
    assert "QB" in levels
    assert levels["QB"] == 3.5 # (5.0 + 2.0) / 2

def test_vorp_calculation():
    replacement_levels = {"WR": 15.0}
    player = {"position": "WR", "total_epa": 45.5}
    
    vorp = AdvancedMetricsEngine.calculate_vorp(player, replacement_levels)
    assert vorp == 30.5

def test_efficiency_index():
    # Standard case
    eff = AdvancedMetricsEngine.calculate_efficiency_index(10.0, 50.0)
    assert eff == 5.0
    
    # Min salary case
    eff_min = AdvancedMetricsEngine.calculate_efficiency_index(0.5, 10.0)
    assert eff_min == 13.333 # 10.0 / 0.75

def test_value_outliers():
    players = [
        {"player": "Star", "position": "QB", "total_epa": 100.0, "cap_hit": 10.0}, # Eff 10
        {"player": "Bust", "position": "QB", "total_epa": 1.0, "cap_hit": 20.0},   # Eff 0.05
        {"player": "Avg1", "position": "QB", "total_epa": 40.0, "cap_hit": 10.0},
        {"player": "Avg2", "position": "QB", "total_epa": 42.0, "cap_hit": 10.0},
        {"player": "Avg3", "position": "QB", "total_epa": 38.0, "cap_hit": 10.0},
    ]
    
    outliers = AdvancedMetricsEngine.identify_value_outliers(players)
    
    assert len(outliers['bargains']) > 0
    assert outliers['bargains'][0]['player'] == "Star"
    assert outliers['albatrosses'][0]['player'] == "Bust"

def test_roster_health_score():
    roster = [{"total_epa": 75.0}, {"total_epa": 75.0}] # Total 150
    needs = {"QB": {"priority": "Low", "group_epa": 50.0}}
    
    score = AdvancedMetricsEngine.calculate_roster_health_score(roster, needs)
    assert score == 100.0
    
    # Test with penalty
    critical_needs = {"QB": {"priority": "Critical", "group_epa": -5.0}}
    score_p = AdvancedMetricsEngine.calculate_roster_health_score(roster, critical_needs)
    assert score_p == 85.0 # 100 - 15
