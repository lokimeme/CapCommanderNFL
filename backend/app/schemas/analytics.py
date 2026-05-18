from pydantic import BaseModel
from typing import List, Optional

class ReplacementLevel(BaseModel):
    position: str
    replacement_epa: float

class VORPReport(BaseModel):
    player: str
    position: str
    total_epa: float
    vorp: float

class HealthScore(BaseModel):
    team: str
    health_score: float
    status: str

class ExitWindow(BaseModel):
    year: int
    savings: float
    dead_cap: float
    efficiency: float
    verdict: str

class PerformanceProjection(BaseModel):
    year: int
    projected_epa: float
    cap_hit: float
    cost_per_epa: float
    is_danger_zone: bool

class ForensicProfile(BaseModel):
    player_name: str
    position: str
    exit_windows: List[ExitWindow]
    performance_projections: List[PerformanceProjection]
    contract_status: str
    remaining_guarantee: float
    guarantee_exposure_pct: float

class FATarget(BaseModel):
    player: str
    position: str
    priority_addressed: str
    cost: float
    epa_gain: float
    value_score: float

class BudgetAllocation(BaseModel):
    total_spendable: float
    reserve_funds: float
    allocation_by_position: dict
    strategy: str
