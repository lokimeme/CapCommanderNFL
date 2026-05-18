from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.app.core.database import get_db
from backend.app.services.market_trends import MarketTrendAnalyzer
from backend.app.models.contract import Contract

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/inflation")
def get_market_inflation(db: Session = Depends(get_db)):
    """
    Returns a positional inflation report based on historical contracts.
    """
    # Fetch historical contracts
    contracts = db.query(Contract).all()
    # Simplified mock year range
    return MarketTrendAnalyzer.calculate_positional_inflation(
        [{"position": c.player.position, "avg_annual": c.avg_annual, "year_signed": c.year_signed} for c in contracts if c.player],
        [2021, 2022, 2023, 2024]
    )

@router.get("/inefficiencies")
def get_market_inefficiencies(db: Session = Depends(get_db)):
    """
    Identifies skewed positional markets across the league.
    """
    contracts = db.query(Contract).all()
    return MarketTrendAnalyzer.detect_market_inefficiencies(
        [{"position": c.player.position, "avg_annual": c.avg_annual} for c in contracts if c.player]
    )
