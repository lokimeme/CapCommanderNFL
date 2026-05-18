from pydantic import BaseModel
from typing import Optional, List
from .team import Team

class PlayerBase(BaseModel):
    gsis_id: str
    name: str
    position: str
    age: Optional[int] = None
    years_exp: Optional[int] = None
    team_abbr: str
    draft_round: Optional[int] = None
    draft_pick: Optional[int] = None

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    team: Optional[Team] = None

    class Config:
        from_attributes = True
