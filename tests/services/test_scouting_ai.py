import pytest
from backend.app.services.scouting_ai import ScoutingAIService

def test_find_statistical_clones():
    target = {"player_id": "P1", "name": "Target", "position": "WR", "total_epa": 80.0, "age": 25}
    pool = [
        {"player_id": "P2", "name": "Clone1", "position": "WR", "total_epa": 78.0, "age": 25}, # Very similar
        {"player_id": "P3", "name": "Diff1", "position": "WR", "total_epa": 10.0, "age": 35},  # Very different
        {"player_id": "P4", "name": "PosDiff", "position": "QB", "total_epa": 80.0, "age": 25}, # Diff position
    ]
    
    clones = ScoutingAIService.find_statistical_clones(target, pool)
    
    assert len(clones) == 1 # Only P2 matches position and is not self
    assert clones[0]['player'] == "Clone1"
    assert clones[0]['similarity_score'] > 90

def test_contract_structure_recommendation():
    profile = {"age": 23, "position": "WR", "target_apy": 20.0} # Young star
    
    res = ScoutingAIService.recommend_contract_structure(profile, {})
    
    assert res['recommended_strategy'] == "Front-Loaded"
    assert res['yearly_hits'][0]['total_cap_hit'] > res['yearly_hits'][3]['total_cap_hit']
    
    # Old star
    old_profile = {"age": 31, "position": "WR", "target_apy": 15.0}
    res_old = ScoutingAIService.recommend_contract_structure(old_profile, {})
    assert res_old['recommended_strategy'] == "Back-Loaded (Incentive heavy)"

def test_identify_market_leaders():
    contracts = [
        {"player": "Highest Paid QB", "position": "QB", "avg_annual": 55.0, "total_guaranteed": 200.0},
        {"player": "Lower Paid QB", "position": "QB", "avg_annual": 40.0, "total_guaranteed": 100.0},
        {"player": "Highest Paid WR", "position": "WR", "avg_annual": 32.0, "total_guaranteed": 80.0},
    ]
    
    leaders = ScoutingAIService.identify_positional_market_leaders(contracts)
    
    assert leaders['QB']['player'] == "Highest Paid QB"
    assert leaders['WR']['player'] == "Highest Paid WR"
