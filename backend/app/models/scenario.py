from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from datetime import datetime

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    team_abbr = Column(String, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("ScenarioTransaction", back_populates="scenario", cascade="all, delete-orphan")

class ScenarioTransaction(Base):
    __tablename__ = "scenario_transactions"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    move_type = Column(String) # CUT, TRADE, RESTRUCTURE, DRAFT
    player_id = Column(String, nullable=True)
    player_name = Column(String, nullable=True)
    savings = Column(Float)
    dead_cap_added = Column(Float)
    details = Column(String, nullable=True) # JSON string or description

    scenario = relationship("Scenario", back_populates="transactions")
