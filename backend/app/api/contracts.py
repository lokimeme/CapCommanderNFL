from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models import contract as contract_model
from backend.app.schemas import contract as contract_schema

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.get("/", response_model=List[contract_schema.Contract])
def read_contracts(skip: int = 0, limit: int = 100, player_id: str = None, team_abbr: str = None, db: Session = Depends(get_db)):
    query = db.query(contract_model.Contract)
    if player_id:
        query = query.filter(contract_model.Contract.player_id == player_id)
    if team_abbr:
        query = query.filter(contract_model.Contract.team_abbr == team_abbr)
    contracts = query.offset(skip).limit(limit).all()
    return contracts

@router.get("/{player_id}", response_model=contract_schema.Contract)
def read_player_contract(player_id: str, db: Session = Depends(get_db)):
    db_contract = db.query(contract_model.Contract).filter(contract_model.Contract.player_id == player_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract
