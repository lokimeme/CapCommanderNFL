import pytest
from backend.app.services.optimizer import RosterOptimizer
from backend.app.models.contract import Contract, ContractYear

def test_optimizer_cap_fix():
    # Mock roster
    # Player 1: High EPA, low salary (Keep)
    # Player 2: Low EPA, high salary (Cut candidate)
    # Player 3: High EPA, high salary (Restructure candidate)
    
    # We need real contract objects for the optimizer
    c2 = Contract(player_id="P2")
    c2.years = [ContractYear(year=2024, cap_number=10.0, signing_bonus=2.0)] # Savings 8.0
    
    c3 = Contract(player_id="P3")
    c3.years = [ContractYear(year=2024, cap_number=20.0, signing_bonus=5.0)]
    
    roster = [
        {"name": "KeepMe", "total_epa": 50.0, "cap_hit": 1.0, "base_salary": 0.8, "contract_obj": Contract()},
        {"name": "CutMe", "total_epa": 1.0, "cap_hit": 10.0, "base_salary": 8.0, "contract_obj": c2},
        {"name": "FixMe", "total_epa": 60.0, "cap_hit": 20.0, "base_salary": 18.0, "contract_obj": c3},
    ]
    
    # Target savings: 5M
    results = RosterOptimizer.find_optimal_cap_fixes(roster, target_savings=5.0)
    
    assert results["is_target_met"] is True
    # The optimizer should prefer restructuring FixMe (high efficiency) or cutting CutMe
    assert len(results["suggested_moves"]) > 0

def test_restructure_candidates():
    roster = [
        {"name": "A", "base_salary": 20.0, "total_epa": 100.0},
        {"name": "B", "base_salary": 2.0, "total_epa": 10.0},
        {"name": "C", "base_salary": 15.0, "total_epa": 5.0},
    ]
    
    candidates = RosterOptimizer.analyze_restructure_candidates(roster)
    
    assert candidates[0]['player'] == "A"
    assert len(candidates) == 2 # Only A and C have salary > 5.0

def test_identify_dead_weight():
    c = Contract(player_id="DW")
    c.years = [ContractYear(year=2024, cap_number=10.0, signing_bonus=2.0)]
    
    roster = [{"name": "DeadWeight", "total_epa": 1.0, "contract_obj": c}]
    
    dw = RosterOptimizer.identify_dead_weight(roster, 2024)
    
    assert len(dw) == 1
    assert dw[0]['player'] == "DeadWeight"
    assert dw[0]['savings_if_cut'] == 8.0
