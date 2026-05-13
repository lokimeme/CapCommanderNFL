import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scripts.utils import format_currency

st.set_page_config(page_title="CapCommander NFL | Roster Forensic Suite", layout="wide", page_icon="🏈")

st.markdown("""
    <style>
    .stMetric {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .status-savings { color: #00ffcc; font-weight: bold; }
    .status-dead { color: #ff4b4b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

DB_PATH = 'data/capcommander.duckdb'

@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(), pd.DataFrame()
    con = duckdb.connect(DB_PATH, read_only=True)
    rosters = con.execute("SELECT * FROM rosters").df()
    contracts = con.execute("SELECT * FROM contracts").df()
    con.close()
    return rosters, contracts

import os

st.title("🏈 CapCommander NFL")
st.subheader("The Roster Forensic & Cap Optimization Suite")

rosters, contracts = load_data()

if rosters.empty or contracts.empty:
    st.warning("Data not found. Please run the ingestion script to populate the database.")
    if st.button("Run Data Ingestion (Mock Mode)"):
        st.info("In real app, this would trigger scripts/ingest_nfl.py...")
        # Placeholder for real data trigger
else:
    # --- DASHBOARD LOGIC ---
    team_list = sorted(rosters['team'].unique())
    selected_team = st.sidebar.selectbox("Select Team", team_list)
    
    # Filter data
    team_roster = rosters[rosters['team'] == selected_team]
    
    st.write(f"### Analyzing {selected_team} Roster")
    
    # ... more UI logic to follow ...
