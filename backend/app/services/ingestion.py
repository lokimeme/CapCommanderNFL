import nfl_data_py as nfl
import pandas as pd
from sqlalchemy.orm import Session
from backend.app.models.team import Team
from backend.app.models.player import Player
from backend.app.models.contract import Contract, ContractYear
from backend.app.models.stats import SeasonalStats
import logging

logger = logging.getLogger("CapCommanderIngestion")

def ingest_teams(db: Session):
    logger.info("Fetching team data...")
    teams_df = nfl.import_team_desc()
    for _, row in teams_df.iterrows():
        existing_team = db.query(Team).filter(Team.team_abbr == row['team_abbr']).first()
        if existing_team:
            existing_team.team_nick = row['team_nick']
            existing_team.team_color = row['team_color']
            existing_team.team_color2 = row['team_color2']
            existing_team.logo_url = row['team_logo_espn']
        else:
            team = Team(
                team_abbr=row['team_abbr'],
                team_nick=row['team_nick'],
                team_color=row['team_color'],
                team_color2=row['team_color2'],
                logo_url=row['team_logo_espn']
            )
            db.add(team)
    db.commit()
    logger.info("Teams ingested successfully.")

def ingest_players_and_contracts(db: Session, years=[2024]):
    logger.info("Fetching roster and contract data...")
    rosters_df = nfl.import_seasonal_rosters(years)
    contracts_df = nfl.import_contracts()
    
    for _, row in rosters_df.iterrows():
        player_id = row['player_id']
        existing_player = db.query(Player).filter(Player.gsis_id == player_id).first()
        if existing_player:
            existing_player.name = row['player_name']
            existing_player.position = row['position']
            existing_player.age = row['age']
            existing_player.years_exp = row['years_exp']
            existing_player.team_abbr = row['team']
        else:
            player = Player(
                gsis_id=player_id,
                name=row['player_name'],
                position=row['position'],
                age=row['age'],
                years_exp=row['years_exp'],
                team_abbr=row['team']
            )
            db.add(player)
            db.flush()
    db.commit()
    
    for _, row in contracts_df.iterrows():
        player_id = row['gsis_id']
        player_exists = db.query(Player).filter(Player.gsis_id == player_id).first()
        if not player_exists:
            continue
            
        # Check if contract already exists
        existing_contract = db.query(Contract).filter(Contract.player_id == player_id).first()
        if existing_contract:
            # Update existing contract
            existing_contract.otc_id = row['otc_id']
            existing_contract.team_abbr = row['team']
            existing_contract.total_value = row['value']
            existing_contract.avg_annual = row['apy']
            existing_contract.total_guaranteed = row['guaranteed']
            existing_contract.contract_length = row['years']
            existing_contract.year_signed = row['year_signed']
            contract = existing_contract
            # Clear old contract years for a fresh update
            db.query(ContractYear).filter(ContractYear.contract_id == contract.id).delete()
        else:
            contract = Contract(
                player_id=player_id,
                otc_id=row['otc_id'],
                team_abbr=row['team'],
                total_value=row['value'],
                avg_annual=row['apy'],
                total_guaranteed=row['guaranteed'],
                contract_length=row['years'],
                year_signed=row['year_signed']
            )
            db.add(contract)
            db.flush()
        
        cols = row.get('cols', [])
        if isinstance(cols, list):
            for year_data in cols:
                contract_year = ContractYear(
                    contract_id=contract.id,
                    year=int(year_data['year']),
                    cap_number=year_data.get('cap_number'),
                    base_salary=year_data.get('base_salary'),
                    signing_bonus=year_data.get('prorated_bonus'),
                    roster_bonus=year_data.get('roster_bonus'),
                    dead_cap=year_data.get('dead_cap'),
                    savings=year_data.get('savings')
                )
                db.add(contract_year)
    
    db.commit()
    logger.info("Players and contracts ingested successfully.")

def ingest_stats(db: Session, years=[2024]):
    logger.info("Fetching seasonal performance data...")
    seasonal_df = nfl.import_seasonal_data(years)
    
    for _, row in seasonal_df.iterrows():
        stats = SeasonalStats(
            player_id=row['player_id'],
            season=row['season'],
            games=row['games'],
            completions=row.get('completions', 0),
            attempts=row.get('attempts', 0),
            passing_yards=row.get('passing_yards', 0),
            passing_tds=row.get('passing_tds', 0),
            interceptions=row.get('interceptions', 0),
            sacks=row.get('sacks', 0),
            carries=row.get('carries', 0),
            rushing_yards=row.get('rushing_yards', 0),
            rushing_tds=row.get('rushing_tds', 0),
            receptions=row.get('receptions', 0),
            receiving_yards=row.get('receiving_yards', 0),
            receiving_tds=row.get('receiving_tds', 0),
            targets=row.get('targets', 0),
            fantasy_points_ppr=row.get('fantasy_points_ppr', 0),
            passing_epa=row.get('passing_epa', 0),
            rushing_epa=row.get('rushing_epa', 0),
            receiving_epa=row.get('receiving_epa', 0),
            total_epa=(row.get('passing_epa', 0) or 0) + (row.get('rushing_epa', 0) or 0) + (row.get('receiving_epa', 0) or 0)
        )
        db.merge(stats)
    db.commit()
    logger.info("Stats ingested successfully.")
