from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    team_abbr: str
    team_nick: str
    team_color: str
    team_color2: str
    logo_url: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int

    class Config:
        from_attributes = True
