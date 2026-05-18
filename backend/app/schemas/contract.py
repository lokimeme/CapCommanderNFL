from pydantic import BaseModel
from typing import Optional, List

class ContractYearBase(BaseModel):
    year: int
    cap_number: Optional[float] = None
    base_salary: Optional[float] = None
    signing_bonus: Optional[float] = None
    roster_bonus: Optional[float] = None
    dead_cap: Optional[float] = None
    savings: Optional[float] = None

class ContractYear(ContractYearBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True

class ContractBase(BaseModel):
    player_id: str
    otc_id: Optional[str] = None
    team_abbr: str
    total_value: Optional[float] = None
    avg_annual: Optional[float] = None
    total_guaranteed: Optional[float] = None
    contract_length: Optional[int] = None
    year_signed: Optional[int] = None

class Contract(ContractBase):
    id: int
    years: List[ContractYear] = []

    class Config:
        from_attributes = True
