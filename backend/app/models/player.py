from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    gsis_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    age = Column(Integer)
    years_exp = Column(Integer)
    team_abbr = Column(String, ForeignKey("teams.team_abbr"))
    draft_round = Column(Integer)
    draft_pick = Column(Integer)

    team = relationship("Team")
    contracts = relationship("Contract", back_populates="player")
    stats = relationship("SeasonalStats", back_populates="player")
