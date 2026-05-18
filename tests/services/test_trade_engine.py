import pytest
from backend.app.services.trade_engine import calculate_player_trade_impact
from backend.app.models.contract import Contract, ContractYear

def test_trade_impact_standard():
    # Mock a contract
    c = Contract(player_id="P1")
    y1 = ContractYear(year=2024, cap_number=10.0, base_salary=8.0, signing_bonus=2.0)
    c.years = [y1]
    
    impact = calculate_player_trade_impact(c, 2024)
    
    # Trading team keeps signing bonus (2.0) as dead cap
    assert impact["trading_team"]["dead_cap_added"] == 2.0
    assert impact["trading_team"]["immediate_savings"] == 8.0 # 10.0 - 2.0
    
    # Receiving team takes the base salary (8.0)
    assert impact["receiving_team"]["new_cap_hit"] == 8.0

def test_trade_impact_with_retention():
    c = Contract(player_id="P1")
    y1 = ContractYear(year=2024, cap_number=10.0, base_salary=8.0, signing_bonus=2.0)
    c.years = [y1]
    
    # 50% retention
    impact = calculate_player_trade_impact(c, 2024, retention_pct=0.5)
    
    # Trading team keeps signing bonus (2.0) + 50% of base salary (4.0) = 6.0
    assert impact["trading_team"]["dead_cap_added"] == 6.0
    assert impact["trading_team"]["immediate_savings"] == 4.0 # 10.0 - 6.0
    
    # Receiving team takes 50% of base salary (4.0)
    assert impact["receiving_team"]["new_cap_hit"] == 4.0
