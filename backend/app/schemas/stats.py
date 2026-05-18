from pydantic import BaseModel
from typing import Optional

class SeasonalStatsBase(BaseModel):
    player_id: str
    season: int
    games: Optional[int] = 0
    completions: Optional[int] = 0
    attempts: Optional[int] = 0
    passing_yards: Optional[float] = 0
    passing_tds: Optional[int] = 0
    interceptions: Optional[int] = 0
    sacks: Optional[float] = 0
    carries: Optional[int] = 0
    rushing_yards: Optional[float] = 0
    rushing_tds: Optional[int] = 0
    receptions: Optional[int] = 0
    receiving_yards: Optional[float] = 0
    receiving_tds: Optional[int] = 0
    targets: Optional[int] = 0
    fantasy_points_ppr: Optional[float] = 0
    passing_epa: Optional[float] = 0
    rushing_epa: Optional[float] = 0
    receiving_epa: Optional[float] = 0
    total_epa: Optional[float] = 0

class SeasonalStats(SeasonalStatsBase):
    id: int

    class Config:
        from_attributes = True
