from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models import stats as stats_model
from backend.app.schemas import stats as stats_schema

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/", response_model=List[stats_schema.SeasonalStats])
def read_stats(skip: int = 0, limit: int = 100, player_id: str = None, season: int = None, db: Session = Depends(get_db)):
    query = db.query(stats_model.SeasonalStats)
    if player_id:
        query = query.filter(stats_model.SeasonalStats.player_id == player_id)
    if season:
        query = query.filter(stats_model.SeasonalStats.season == season)
    stats = query.offset(skip).limit(limit).all()
    return stats

@router.get("/top-epa", response_model=List[stats_schema.SeasonalStats])
def read_top_epa(limit: int = 10, season: int = 2023, db: Session = Depends(get_db)):
    stats = db.query(stats_model.SeasonalStats).filter(
        stats_model.SeasonalStats.season == season
    ).order_by(stats_model.SeasonalStats.total_epa.desc()).limit(limit).all()
    return stats
