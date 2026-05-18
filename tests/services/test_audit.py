import pytest
from backend.app.services.audit import LeagueFinancialAudit

def test_parity_index():
    team_caps = [
        {"team_abbr": "KC", "cap_space": 10.0},
        {"team_abbr": "CHI", "cap_space": 80.0}, # Rich
        {"team_abbr": "BUF", "cap_space": -20.0}, # Poor
    ]
    
    parity = LeagueFinancialAudit.calculate_parity_index(team_caps)
    
    assert parity['spread_range'] == 100.0
    assert parity['standard_deviation'] > 0
    assert "gini_index" in parity

def test_audit_exposure():
    contracts = [
        {"position": "QB", "total_guaranteed": 150.0},
        {"position": "WR", "total_guaranteed": 50.0},
        {"position": "QB", "total_guaranteed": 200.0},
    ]
    
    audit = LeagueFinancialAudit.audit_guaranteed_exposure(contracts)
    
    assert audit['league_total_debt'] == 400.0
    assert audit['positional_concentration']['QB'] == 350.0

def test_identify_red_flags():
    teams = [
        {"team_abbr": "Saints", "dead_cap": 50.0, "future_obligations": 300.0, "roster_health_score": 45.0}, # Critical
        {"team_abbr": "Texans", "dead_cap": 5.0, "future_obligations": 100.0, "roster_health_score": 90.0},  # Safe
    ]
    
    flags = LeagueFinancialAudit.identify_financial_red_flags(teams)
    
    assert len(flags) == 1
    assert flags[0]['team'] == "Saints"
    assert flags[0]['risk_level'] == "Critical"
    assert len(flags[0]['red_flags']) == 3
