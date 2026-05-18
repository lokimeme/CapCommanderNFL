import pytest
from backend.app.services.forensic_pro import ForensicScoutingService
from backend.app.models.contract import Contract, ContractYear

def test_player_forensic_report_generation():
    player = {"name": "Star Player", "age": 25, "position": "QB", "total_epa": 150.0}
    
    # Mock complex multi-year contract
    c = Contract(player_id="P1", total_value=160.0, total_guaranteed=100.0)
    c.years = [
        ContractYear(year=2024, cap_number=40.0, base_salary=30.0, signing_bonus=10.0),
        ContractYear(year=2025, cap_number=40.0, base_salary=30.0, signing_bonus=10.0),
        ContractYear(year=2026, cap_number=40.0, base_salary=30.0, signing_bonus=10.0),
        ContractYear(year=2027, cap_number=40.0, base_salary=30.0, signing_bonus=10.0),
    ]
    
    report = ForensicScoutingService.generate_player_forensic_report(player, c, 2024)
    
    assert report['player_name'] == "Star Player"
    assert len(report['exit_windows']) == 4
    assert report['financial_summary']['contract_status'] == "Secure"
    # Guaranteed exposure check
    assert report['financial_summary']['remaining_guarantee'] == 100.0

def test_identify_exit_year():
    player = {"name": "Old Vet", "age": 33, "position": "RB", "total_epa": 20.0}
    c = Contract(player_id="P2", total_value=20.0)
    c.years = [
        ContractYear(year=2024, cap_number=10.0, base_salary=9.0, signing_bonus=1.0), # Savings 9.0
        ContractYear(year=2025, cap_number=10.0, base_salary=1.0, signing_bonus=9.0), # Savings 1.0 (Low efficiency)
    ]
    
    report = ForensicScoutingService.generate_player_forensic_report(player, c, 2024)
    exit_year = ForensicScoutingService.identify_optimal_exit_year(report)
    
    assert exit_year == 2024

def test_cliff_prediction_logic():
    player = {"name": "Aging WR", "age": 31, "position": "WR", "total_epa": 80.0}
    c = Contract(player_id="P3")
    c.years = [
        ContractYear(year=2024, cap_number=20.0, base_salary=15.0),
        ContractYear(year=2025, cap_number=22.0, base_salary=17.0),
        ContractYear(year=2026, cap_number=25.0, base_salary=20.0),
    ]
    
    report = ForensicScoutingService.generate_player_forensic_report(player, c, 2024)
    cliffs = report['performance_projections']
    
    # Check if EPA declines and Danger Zone is eventually hit
    assert cliffs[2]['projected_epa'] < cliffs[0]['projected_epa']
    # At 33 with a 25M cap hit, it should hit a danger zone
    assert any(cl['is_danger_zone'] for cl in cliffs)
