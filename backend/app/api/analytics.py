from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.app.core.database import get_db
from backend.app.services.analytics import AdvancedMetricsEngine
from backend.app.models.player import Player
from backend.app.models.stats import SeasonalStats

router = APIRouter(prefix="/analytics", tags=["analytics"])

from backend.app.services.compliance import CBAComplianceEngine
from backend.app.services.injury_risk import InjuryRiskModel

@router.get("/vorp")
def get_vorp_report(team_abbr: str = None, db: Session = Depends(get_db)):
    all_stats_query = db.query(SeasonalStats, Player).join(Player, SeasonalStats.player_id == Player.gsis_id)
    all_data = [{"position": p.position, "total_epa": s.total_epa} for s, p in all_stats_query.all()]
    replacement_levels = AdvancedMetricsEngine.calculate_positional_replacement_level(all_data)
    
    query = all_stats_query
    if team_abbr: query = query.filter(Player.team_abbr == team_abbr)
        
    results = []
    for s, p in query.all():
        vorp = AdvancedMetricsEngine.calculate_vorp({"position": p.position, "total_epa": s.total_epa}, replacement_levels)
        results.append({
            "player": p.name, "position": p.position, "total_epa": s.total_epa, "vorp": vorp
        })
    return sorted(results, key=lambda x: x['vorp'], reverse=True)

@router.get("/health/{team_abbr}")
def get_team_health(team_abbr: str, db: Session = Depends(get_db)):
    # Fetch team roster
    players = db.query(Player).filter(Player.team_abbr == team_abbr).all()
    roster_data = [{"position": p.position, "name": p.name} for p in players]
    
    compliance = CBAComplianceEngine.check_roster_validity(roster_data)
    
    # Calculate health score based on compliance and total count
    base_score = 100
    penalty = len(compliance['warnings']) * 10
    score = max(0, base_score - penalty)
    
    return {
        "team": team_abbr,
        "health_score": score,
        "status": "Healthy" if score > 80 else "Attention Required" if score > 50 else "Critical",
        "compliance": compliance
    }

from backend.app.services.historical_analysis import HistoricalCapBenchmarks

@router.get("/benchmarks/{team_abbr}")
def get_historical_benchmarks(team_abbr: str, db: Session = Depends(get_db)):
    players = db.query(Player, Contract).filter(
        Player.team_abbr == team_abbr
    ).join(Contract, Player.gsis_id == Contract.player_id).all()
    
    roster_cap = []
    for p, c in players:
        y2026 = next((y for y in c.years if y.year == 2026), None)
        cap_hit = y2026.cap_number if y2026 else c.avg_annual
        roster_cap.append({"position": p.position, "cap_hit": cap_hit})
        
    analysis = HistoricalCapBenchmarks.analyze_roster_allocation(roster_cap)
    return analysis
