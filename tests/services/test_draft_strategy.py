import pytest
from backend.app.services.draft_strategy import DraftStrategyService

def test_trade_up_cost():
    target = 10 # Value ~1300
    team_picks = [20, 52, 84] # Values ~850, ~380, ~170 = 1400
    
    result = DraftStrategyService.calculate_trade_up_cost(target, team_picks)
    
    assert result["is_feasible"] is True
    assert 20 in result["suggested_package"]
    assert 52 in result["suggested_package"]
    assert result["package_value"] >= 1300

def test_trade_down_scenarios():
    scenarios = DraftStrategyService.suggest_trade_down_scenarios(15)
    
    assert len(scenarios) == 3
    # Check that all have equity ratios around 1.0
    for s in scenarios:
        assert 0.8 <= s["equity_ratio"] <= 1.5

def test_pick_distribution_analysis():
    picks = [5, 37, 69, 101, 133] # A top-heavy but volume draft
    
    analysis = DraftStrategyService.analyze_pick_value_distribution(picks)
    
    assert analysis["total_capital"] > 0
    assert analysis["capital_concentration"] > 0.5
    assert "strategy" in analysis or "draft_identity" in analysis

def test_pro_bowl_probability():
    p1 = DraftStrategyService.estimate_pro_bowl_probability(1)
    p32 = DraftStrategyService.estimate_pro_bowl_probability(32)
    p100 = DraftStrategyService.estimate_pro_bowl_probability(100)
    p250 = DraftStrategyService.estimate_pro_bowl_probability(250)
    
    assert p1 > p32 > p100 > p250
    assert 0.01 <= p250 <= 0.05
    assert 0.60 <= p1 <= 0.80
