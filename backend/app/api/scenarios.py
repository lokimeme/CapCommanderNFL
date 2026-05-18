from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models import scenario as scenario_model
from backend.app.schemas import scenario as scenario_schema

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

@router.get("/", response_model=List[scenario_schema.Scenario])
def read_scenarios(team_abbr: str = None, db: Session = Depends(get_db)):
    query = db.query(scenario_model.Scenario)
    if team_abbr:
        query = query.filter(scenario_model.Scenario.team_abbr == team_abbr)
    return query.all()

@router.post("/", response_model=scenario_schema.Scenario)
def create_scenario(scenario: scenario_schema.ScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = scenario_model.Scenario(
        team_abbr=scenario.team_abbr,
        name=scenario.name
    )
    db.add(db_scenario)
    db.flush()
    
    for t in scenario.transactions:
        db_transaction = scenario_model.ScenarioTransaction(
            scenario_id=db_scenario.id,
            **t.dict()
        )
        db.add(db_transaction)
    
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    db_scenario = db.query(scenario_model.Scenario).filter(scenario_model.Scenario.id == scenario_id).first()
    if not db_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    db.delete(db_scenario)
    db.commit()
    return {"message": "Scenario deleted"}
