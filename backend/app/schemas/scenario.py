from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TransactionBase(BaseModel):
    move_type: str
    player_id: Optional[str] = None
    player_name: Optional[str] = None
    savings: float
    dead_cap_added: float
    details: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    scenario_id: int

    class Config:
        from_attributes = True

class ScenarioBase(BaseModel):
    team_abbr: str
    name: str

class ScenarioCreate(ScenarioBase):
    transactions: List[TransactionBase] = []

class Scenario(ScenarioBase):
    id: int
    created_at: datetime
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True
