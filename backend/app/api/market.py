from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict
from backend.app.core.database import get_db
from backend.app.services.market_trends import MarketTrendAnalyzer
from backend.app.models.contract import Contract
from backend.app.models.player import Player

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/inflation")
def get_market_inflation(db: Session = Depends(get_db)):
    """
    Returns a positional inflation report based on historical contracts.
    """
    # Fetch historical contracts with joined player data to avoid N+1 queries
    # Filter for years we care about to reduce data volume
    contracts = db.query(Contract).options(joinedload(Contract.player)).filter(Contract.year_signed >= 2021).all()
    
    # Process data efficiently
    contract_data = []
    for c in contracts:
        if c.player:
            contract_data.append({
                "position": c.player.position, 
                "avg_annual": c.avg_annual, 
                "year_signed": c.year_signed
            })
            
    return MarketTrendAnalyzer.calculate_positional_inflation(
        contract_data,
        [2021, 2022, 2023, 2024]
    )

@router.get("/inefficiencies")
def get_market_inefficiencies(db: Session = Depends(get_db)):
    """
    Identifies skewed positional markets across the league.
    """
    contracts = db.query(Contract).options(joinedload(Contract.player)).all()
    
    contract_data = []
    for c in contracts:
        if c.player:
            contract_data.append({
                "position": c.player.position, 
                "avg_annual": c.avg_annual
            })
            
    return MarketTrendAnalyzer.detect_market_inefficiencies(contract_data)
