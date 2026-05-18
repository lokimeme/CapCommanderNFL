import pytest
from backend.app.services.cba_incentives import CBAIncentiveService

def test_incentive_status_evaluation():
    prev_stats = {"passing_tds": 30}
    criteria = {"metric": "passing_tds", "threshold": 25, "value": 1.0}
    
    status = CBAIncentiveService.evaluate_incentive_status(prev_stats, criteria)
    assert status == "LTBE"
    
    criteria_high = {"metric": "passing_tds", "threshold": 35, "value": 1.0}
    status_high = CBAIncentiveService.evaluate_incentive_status(prev_stats, criteria_high)
    assert status_high == "NLTBE"

def test_incentive_cap_impact():
    incentives = [
        {"status": "LTBE", "value": 2.0},
        {"status": "NLTBE", "value": 5.0},
        {"status": "LTBE", "value": 1.5},
    ]
    
    impact = CBAIncentiveService.calculate_cap_impact(incentives)
    assert impact["immediate_charge"] == 3.5
    assert impact["deferred_potential"] == 5.0

def test_end_of_year_adjustments():
    contract_inc = [
        {"metric": "games", "threshold": 10, "value": 1.0, "status": "LTBE"},
        {"metric": "sacks", "threshold": 10, "value": 2.0, "status": "NLTBE"},
    ]
    
    # Scenario: Played 8 games (failed LTBE), recorded 12 sacks (achieved NLTBE)
    actual = {"games": 8, "sacks": 12}
    
    adj = CBAIncentiveService.process_end_of_year_adjustments(actual, contract_inc)
    
    # LTBE failed = +1.0 Credit
    # NLTBE earned = -2.0 Debit
    # Net = -1.0
    assert adj["next_year_adjustment"] == -1.0
    assert len(adj["adjustment_details"]) == 2

def test_incentive_scenarios():
    contract_inc = [{"metric": "yards", "threshold": 1000, "value": 1.0, "status": "NLTBE"}]
    scenarios = [
        {"name": "Big Year", "stats": {"yards": 1200}},
        {"name": "Injury Year", "stats": {"yards": 200}}
    ]
    
    results = CBAIncentiveService.simulate_incentive_scenarios(contract_inc, scenarios)
    
    assert len(results) == 2
    assert results[0]["net_adjustment"] == -1.0 # Debit
    assert results[1]["net_adjustment"] == 0.0  # No change
