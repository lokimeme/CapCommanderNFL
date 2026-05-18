from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models import player as player_model
from backend.app.schemas import player as player_schema

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=List[player_schema.Player])
def read_players(skip: int = 0, limit: int = 100, team_abbr: str = None, db: Session = Depends(get_db)):
    query = db.query(player_model.Player)
    if team_abbr: query = query.filter(player_model.Player.team_abbr == team_abbr)
    return query.offset(skip).limit(limit).all()

@router.get("/{gsis_id}", response_model=player_schema.Player)
def read_player(gsis_id: str, db: Session = Depends(get_db)):
    db_player = db.query(player_model.Player).filter(player_model.Player.gsis_id == gsis_id).first()
    if db_player is None: raise HTTPException(status_code=404, detail="Player not found")
    return db_player
