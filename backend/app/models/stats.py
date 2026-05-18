from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class SeasonalStats(Base):
    __tablename__ = "seasonal_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, ForeignKey("players.gsis_id"))
    season = Column(Integer)
    games = Column(Integer)
    completions = Column(Integer)
    attempts = Column(Integer)
    passing_yards = Column(Float)
    passing_tds = Column(Integer)
    interceptions = Column(Integer)
    sacks = Column(Float)
    carries = Column(Integer)
    rushing_yards = Column(Float)
    rushing_tds = Column(Integer)
    receptions = Column(Integer)
    receiving_yards = Column(Float)
    receiving_tds = Column(Integer)
    targets = Column(Integer)
    fantasy_points_ppr = Column(Float)
    passing_epa = Column(Float)
    rushing_epa = Column(Float)
    receiving_epa = Column(Float)
    total_epa = Column(Float)

    player = relationship("Player", back_populates="stats")
