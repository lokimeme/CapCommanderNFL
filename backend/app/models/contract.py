from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, ForeignKey("players.gsis_id"))
    otc_id = Column(String)
    team_abbr = Column(String)
    total_value = Column(Float)
    avg_annual = Column(Float)
    total_guaranteed = Column(Float)
    contract_length = Column(Integer)
    year_signed = Column(Integer)

    player = relationship("Player", back_populates="contracts")
    years = relationship("ContractYear", back_populates="contract")

class ContractYear(Base):
    __tablename__ = "contract_years"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    year = Column(Integer)
    cap_number = Column(Float)
    base_salary = Column(Float)
    signing_bonus = Column(Float)
    roster_bonus = Column(Float)
    option_bonus = Column(Float)
    workout_bonus = Column(Float)
    dead_cap = Column(Float)
    savings = Column(Float)

    contract = relationship("Contract", back_populates="years")
