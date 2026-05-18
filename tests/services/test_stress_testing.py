import pytest
from backend.app.services.stress_testing import SyntheticDataGenerator, OffseasonBattleSimulator

def test_data_generation_volume():
    players = SyntheticDataGenerator.generate_bulk_players(100)
    contracts = SyntheticDataGenerator.generate_bulk_contracts(players)
    stats = SyntheticDataGenerator.generate_bulk_stats(players)
    
    assert len(players) == 100
    assert len(contracts) == 100
    assert len(stats) == 100
    
    # Verify contract years
    assert len(contracts[0]['years']) >= 1
    assert contracts[0]['total_value'] > 0

def test_battle_simulation_parity():
    # Generate mock league
    players = SyntheticDataGenerator.generate_bulk_players(200)
    contracts = SyntheticDataGenerator.generate_bulk_contracts(players)
    stats = SyntheticDataGenerator.generate_bulk_stats(players)
    
    sim = OffseasonBattleSimulator(league_cap=150.0) # Tight cap to force optimization
    sim.run_league_simulation(players, contracts, stats)
    
    results = sim.results
    assert len(results) > 0
    # At least one team should be optimized or compliant
    assert any(r['status'] in ["Fixed", "Compliant"] for r in results.values())

def test_simulation_report_generation():
    players = SyntheticDataGenerator.generate_bulk_players(50)
    contracts = SyntheticDataGenerator.generate_bulk_contracts(players)
    stats = SyntheticDataGenerator.generate_bulk_stats(players)
    
    sim = OffseasonBattleSimulator()
    sim.run_league_simulation(players, contracts, stats)
    
    report = sim.get_simulation_report()
    assert "LEAGUE-WIDE OFFSEASON BATTLE REPORT" in report
    assert "Total Teams Processed" in report
