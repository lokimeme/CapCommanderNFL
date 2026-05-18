from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.ingestion import ingest_teams, ingest_players_and_contracts, ingest_stats
import logging

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger("CapCommanderAdmin")

def full_sync_task(db_url: str):
    """
    Background task to run full ingestion.
    We pass db_url because BackgroundTasks might outlive the request session.
    """
    from backend.app.core.database import SessionLocal
    db = SessionLocal()
    try:
        logger.info("Starting background full sync...")
        ingest_teams(db)
        ingest_players_and_contracts(db)
        ingest_stats(db)
        logger.info("Background sync complete.")
    except Exception as e:
        logger.error(f"Background sync failed: {e}")
    finally:
        db.close()

@router.post("/sync")
async def trigger_sync(background_tasks: BackgroundTasks):
    """
    Triggers a full data ingestion in the background.
    """
    background_tasks.add_task(full_sync_task, "placeholder")
    return {"message": "Full sync triggered in the background. Roster data will refresh shortly."}
