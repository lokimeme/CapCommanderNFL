from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.app.core.database import get_db
from backend.app.services.analytics import AdvancedMetricsEngine
from backend.app.models.player import Player
from backend.app.models.stats import SeasonalStats

router = APIRouter(prefix="/analytics", tags=["analytics"])

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
    return {"team": team_abbr, "health_score": 82.5, "status": "Contender"}
