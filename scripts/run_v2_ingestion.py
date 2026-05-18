from backend.app.core.database import SessionLocal, engine, Base
from backend.app.services.ingestion import ingest_teams, ingest_players_and_contracts, ingest_stats
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CapCommanderRunner")

def run_ingestion():
    # Ensure tables are created
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        ingest_teams(db)
        ingest_players_and_contracts(db)
        ingest_stats(db)
        logger.info("Full ingestion cycle complete.")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_ingestion()
