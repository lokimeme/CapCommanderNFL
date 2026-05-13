import nfl_data_py as nfl
import duckdb
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CapCommanderIngest")

DB_PATH = 'data/capcommander.duckdb'

def setup_db():
    if not os.path.exists('data'):
        os.makedirs('data')
    con = duckdb.connect(DB_PATH)
    logger.info("Database initialized at " + DB_PATH)
    con.close()

def ingest_nfl_data(years=[2023, 2024]):
    logger.info(f"Starting data ingestion for years: {years}")
    
    # 1. Import Rosters (Seasonal)
    logger.info("Fetching roster data...")
    rosters_df = nfl.import_seasonal_rosters(years)
    
    # 2. Import Contracts
    logger.info("Fetching contract data from OverTheCap...")
    contracts_df = nfl.import_contracts()
    
    # 3. Import Depth Charts
    logger.info("Fetching depth charts...")
    depth_charts_df = nfl.import_depth_charts(years)
    
    # 4. Save to DuckDB
    con = duckdb.connect(DB_PATH)
    
    logger.info("Saving rosters to DuckDB...")
    con.execute("CREATE OR REPLACE TABLE rosters AS SELECT * FROM rosters_df")
    
    logger.info("Saving contracts to DuckDB...")
    con.execute("CREATE OR REPLACE TABLE contracts AS SELECT * FROM contracts_df")
    
    logger.info("Saving depth charts to DuckDB...")
    con.execute("CREATE OR REPLACE TABLE depth_charts AS SELECT * FROM depth_charts_df")
    
    con.close()
    logger.info("Ingestion complete.")

if __name__ == "__main__":
    setup_db()
    ingest_nfl_data()
