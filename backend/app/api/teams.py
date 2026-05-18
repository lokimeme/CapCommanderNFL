from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models import team as team_model
from backend.app.schemas import team as team_schema

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=List[team_schema.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = db.query(team_model.Team).offset(skip).limit(limit).all()
    return teams

@router.get("/{team_abbr}", response_model=team_schema.Team)
def read_team(team_abbr: str, db: Session = Depends(get_db)):
    db_team = db.query(team_model.Team).filter(team_model.Team.team_abbr == team_abbr).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team
