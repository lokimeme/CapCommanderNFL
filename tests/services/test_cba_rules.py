import pytest
from backend.app.services.cba_rules import calculate_detailed_cut_impact, estimate_franchise_tag, calculate_fifth_year_option
from backend.app.models.contract import Contract, ContractYear
from backend.app.models.player import Player

def test_franchise_tag_estimates():
    assert estimate_franchise_tag("QB", 2024) == 38.3
    assert estimate_franchise_tag("WR", 2024) == 21.8
    assert estimate_franchise_tag("UNKNOWN", 2024) == 15.0

def test_fifth_year_option():
    # Mock a first round player
    p1 = Player(draft_round=1, position="QB")
    val = calculate_fifth_year_option(p1, "Basic")
    assert val == 20.0
    
    val_pb = calculate_fifth_year_option(p1, "2+ Pro Bowls")
    assert val_pb == 30.0 # 20.0 * 1.5
    
    # Mock a non-first round player
    p2 = Player(draft_round=2, position="QB")
    assert calculate_fifth_year_option(p2) is None

def test_cut_impact_logic():
    # Mock a contract with 2 years
    c = Contract(player_id="P1")
    y1 = ContractYear(year=2024, cap_number=10.0, signing_bonus=2.0)
    y2 = ContractYear(year=2025, cap_number=12.0, signing_bonus=2.0)
    c.years = [y1, y2]
    
    impact = calculate_detailed_cut_impact(c, 2024)
    
    # Pre-June 1: All signing bonus accelerates (2.0 + 2.0 = 4.0)
    assert impact["pre_june_1"]["dead_cap"] == 4.0
    assert impact["pre_june_1"]["savings"] == 6.0 # 10.0 - 4.0
    
    # Post-June 1: Only current year signing bonus hits (2.0)
    assert impact["post_june_1"]["dead_cap_current"] == 2.0
    assert impact["post_june_1"]["dead_cap_future"] == 2.0
    assert impact["post_june_1"]["savings"] == 8.0 # 10.0 - 2.0
