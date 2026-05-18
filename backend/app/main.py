from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.app.core.database import engine, Base
from backend.app.models import team, player, contract, stats, scenario
from backend.app.api import teams, players, contracts, stats as stats_api, scenarios, admin, analytics, strategy, market
from backend.app.core.middleware import LoggingMiddleware
import logging

# Initialize Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("CapCommanderMain")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CapCommander API", 
    version="2.4.0",
    description="Enterprise-grade NFL Front Office Financial Engine"
)

app.add_middleware(LoggingMiddleware)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred in the CapCommander Engine."},
    )

@app.get("/")
async def root():
    return {
        "status": "online",
        "engine_version": "2.4.0-enterprise",
        "documentation": "/docs"
    }

app.include_router(teams.router)
app.include_router(players.router)
app.include_router(contracts.router)
app.include_router(stats_api.router)
app.include_router(scenarios.router)
app.include_router(admin.router)
app.include_router(analytics.router)
app.include_router(strategy.router)
app.include_router(market.router)
