from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.app.core.database import get_db
from backend.app.services.free_agency import FreeAgencyRecommendationEngine
from backend.app.services.team_needs import TeamNeedsService
from backend.app.models.player import Player
from backend.app.models.contract import Contract
from backend.app.models.stats import SeasonalStats

router = APIRouter(prefix="/free-agency", tags=["free-agency"])

@router.get("/recommendations/{team_abbr}")
def get_fa_recommendations(team_abbr: str, db: Session = Depends(get_db)):
    # 1. Fetch team roster and stats
    results = db.query(Player, Contract, SeasonalStats).filter(
        Player.team_abbr == team_abbr
    ).join(Contract, Player.gsis_id == Contract.player_id).join(
        SeasonalStats, Player.gsis_id == SeasonalStats.player_id
    ).all()
    
    roster_stats = []
    total_cap_used = 0
    for p, c, s in results:
        # Use 2026 cap hit as we shifted the sim year
        y2026 = next((y for y in c.years if y.year == 2026), None)
        cap_hit = y2026.cap_number if y2026 else c.avg_annual
        roster_stats.append({
            "player_id": p.gsis_id,
            "position": p.position,
            "total_epa": s.total_epa,
            "cap_hit": cap_hit
        })
        total_cap_used += cap_hit

    # 2. Calculate Team Needs
    needs = TeamNeedsService.calculate_positional_needs(roster_stats)
    
    # 3. Available Free Agent Pool (Mocked for Demo)
    # In a real app, this would be a separate table or external API
    available_fas = [
        {"name": "Josh Allen", "position": "DL", "projected_apy": 28.5, "total_epa": 22.4},
        {"name": "Brian Burns", "position": "DL", "projected_apy": 26.0, "total_epa": 18.5},
        {"name": "Tee Higgins", "position": "WR", "projected_apy": 21.5, "total_epa": 15.2},
        {"name": "Chris Jones", "position": "DL", "projected_apy": 31.0, "total_epa": 25.1},
        {"name": "Jaylon Johnson", "position": "DB", "projected_apy": 19.0, "total_epa": 14.8},
        {"name": "Kirk Cousins", "position": "QB", "projected_apy": 40.0, "total_epa": 32.1},
        {"name": "Saquon Barkley", "position": "RB", "projected_apy": 12.5, "total_epa": 11.2},
        {"name": "Tyron Smith", "position": "OL", "projected_apy": 12.0, "total_epa": 9.5},
        {"name": "Patrick Queen", "position": "LB", "projected_apy": 14.0, "total_epa": 10.8},
        {"name": "Antoine Winfield Jr.", "position": "DB", "projected_apy": 18.0, "total_epa": 16.2},
        {"name": "Baker Mayfield", "position": "QB", "projected_apy": 32.5, "total_epa": 21.4},
        {"name": "Christian Wilkins", "position": "DL", "projected_apy": 24.0, "total_epa": 14.5},
        {"name": "L'Jarius Sneed", "position": "DB", "projected_apy": 18.5, "total_epa": 13.9},
        {"name": "Mike Evans", "position": "WR", "projected_apy": 23.0, "total_epa": 17.8}
    ]
    
    # 4. Run Recommendation Engine
    # Assume a standard remaining budget of $50M for the demo
    budget = 50.0 
    targets = FreeAgencyRecommendationEngine.identify_target_free_agents(needs, available_fas, budget)
    
    return {
        "team_abbr": team_abbr,
        "needs": needs,
        "recommendations": targets[:3] # Return top 3
    }
