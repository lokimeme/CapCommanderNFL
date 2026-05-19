from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.app.core.database import get_db
from backend.app.services.optimizer import RosterOptimizer
from backend.app.services.draft_strategy import DraftStrategyService
from backend.app.models.player import Player
from backend.app.models.contract import Contract
from backend.app.models.stats import SeasonalStats

router = APIRouter(prefix="/strategy", tags=["strategy"])

@router.get("/optimize/{team_abbr}")
def optimize_roster(team_abbr: str, target: float, db: Session = Depends(get_db)):
    players = db.query(Player, Contract, SeasonalStats).filter(
        Player.team_abbr == team_abbr
    ).join(Contract, Player.gsis_id == Contract.player_id).join(
        SeasonalStats, Player.gsis_id == SeasonalStats.player_id
    ).all()
    
    roster_data = []
    for p, c, s in players:
        y2026 = next((y for y in c.years if y.year == 2026), None)
        if y2026:
            roster_data.append({
                "name": p.name, "cap_hit": y2026.cap_number, "base_salary": y2026.base_salary,
                "total_epa": s.total_epa, "contract_obj": c
            })
    return RosterOptimizer.find_optimal_cap_fixes(roster_data, target)

@router.post("/draft/trade-up")
def evaluate_trade_up(target_pick: int, team_picks: List[int]):
    return DraftStrategyService.calculate_trade_up_cost(target_pick, team_picks)
