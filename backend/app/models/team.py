from sqlalchemy import Column, String, Integer
from backend.app.core.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_abbr = Column(String, unique=True, index=True)
    team_nick = Column(String)
    team_color = Column(String)
    team_color2 = Column(String)
    logo_url = Column(String)
