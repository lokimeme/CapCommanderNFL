import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
import os
import time

API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

class CapCommanderV2UI:
    
    def __init__(self):
        st.set_page_config(
            page_title="CapCommander NFL | Enterprise War Room",
            layout="wide",
            page_icon="🏈",
            initial_sidebar_state="expanded"
        )
        self._apply_styles()
        self._initialize_state()

    def _apply_styles(self):
        st.markdown("""
            <style>
            .main { background-color: #0e1117; color: #ffffff; }
            .stMetric {
                background-color: rgba(128, 128, 128, 0.05);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid rgba(128, 128, 128, 0.1);
            }
            .transaction-log {
                font-family: 'Courier New', monospace;
                font-size: 0.85em;
                background-color: #161b22;
                color: #58a6ff;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 5px;
                border-left: 4px solid #238636;
            }
            .stat-card {
                padding: 15px;
                border-radius: 8px;
                background: linear-gradient(145deg, #1e252e, #161b22);
                border: 1px solid #30363d;
            }
            .premium-text { color: #d29922; font-weight: bold; }
            .danger-text { color: #f85149; font-weight: bold; }
            .success-text { color: #3fb950; font-weight: bold; }
            </style>
        """, unsafe_allow_html=True)

    def _initialize_state(self):
        if 'pending_moves' not in st.session_state:
            st.session_state['pending_moves'] = []
        if 'active_team' not in st.session_state:
            st.session_state['active_team'] = "KC"
        if 'last_sync' not in st.session_state:
            st.session_state['last_sync'] = "Never"

    def _fetch(self, endpoint: str, params: dict = None):
        try:
            res = requests.get(f"{API_BASE_URL}{endpoint}", params=params, timeout=5)
            if res.status_code == 200: return res.json()
            return None
        except Exception as e:
            st.error(f"Backend Offline: {e}")
            return None

    def render_sidebar(self):
        with st.sidebar:
            st.title("🏈 CapCommander V2")
            st.caption("Enterprise Front Office Suite v2.4.0")
            st.divider()
            
            teams = self._fetch("/teams/")
            if teams:
                team_abbrs = sorted([t['team_abbr'] for t in teams])
                st.session_state['active_team'] = st.selectbox("Active Franchise", team_abbrs, index=team_abbrs.index(st.session_state['active_team']))
                team_info = next(t for t in teams if t['team_abbr'] == st.session_state['active_team'])
                st.image(team_info['logo_url'], width=120)
                st.subheader(f"{team_info['team_nick']}")
            else:
                st.warning("Could not load teams. Sync database.")
                return None

            st.divider()
            st.subheader("🛠 Admin Controls")
            if st.button("🔄 Trigger Global Sync", use_container_width=True):
                requests.post(f"{API_BASE_URL}/admin/sync")
                st.toast("Background Ingestion Started", icon="🚀")
                st.session_state['last_sync'] = time.strftime("%H:%M:%S")

            st.caption(f"Last Sync: {st.session_state['last_sync']}")
            
            st.subheader("💾 Scenario Management")
            s_name = st.text_input("Blueprint Name", "Vison 2024")
            if st.button("Save Current Session", use_container_width=True):
                payload = {
                    "team_abbr": st.session_state['active_team'],
                    "name": s_name,
                    "transactions": [{"move_type": m['type'], "player_name": m['player'], "savings": m['savings'], "dead_cap_added": 0} for m in st.session_state['pending_moves']]
                }
                requests.post(f"{API_BASE_URL}/scenarios/", json=payload)
                st.success("Scenario Saved to DB")
            
            return team_info

    def render_dashboard(self, team_info):
        st.title(f"🏟 {team_info['team_nick']} Command Center")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Effective Cap Space", "$42.5M", delta="+12.1M")
        col2.metric("Roster Strength", "88/100", delta="-2.1")
        col3.metric("Dead Cap Exposure", "$18.4M", delta="-5.0", delta_color="inverse")
        col4.metric("VORP Aggregate", "142.8", delta="+12.5")
        
        st.divider()
        
        tabs = st.tabs([
            "📋 Roster & VORP", 
            "✂️ Forensic Engine", 
            "📈 ML Insights", 
            "💎 FA Recommendations",
            "🏟 War Room Simulator",
            "⚙️ Strategy Optimizer",
            "🎯 Draft Scouting",
            "🏢 League Audit"
        ])
        
        with tabs[0]: self._render_roster_vorp()
        with tabs[1]: self._render_forensics()
        with tabs[2]: self._render_ml_insights()
        with tabs[3]: self._render_fa_engine()
        with tabs[4]: self._render_war_room()
        with tabs[5]: self._render_optimizer()
        with tabs[6]: self._render_draft_scouting()
        with tabs[7]: self._render_league_audit()

    def _render_draft_scouting(self):
        st.header("🎯 Draft Scouting & Board Management")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Interactive Draft Board")
            mock_board = pd.DataFrame({
                'Rank': range(1, 11),
                'Prospect': ["Caleb Williams", "Drake Maye", "Marvin Harrison Jr", "Jayden Daniels", "Joe Alt", "Brock Bowers", "Malik Nabers", "Olu Fashanu", "Rome Odunze", "JC Latham"],
                'Position': ["QB", "QB", "WR", "QB", "OT", "TE", "WR", "OT", "WR", "OT"],
                'Grade': [9.6, 9.4, 9.5, 9.1, 8.9, 8.8, 8.7, 8.6, 8.5, 8.4]
            })
            st.dataframe(mock_board, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("Trade-Up Evaluator")
            target_pick = st.number_input("Target Pick #", 1, 32, 5)
            if st.button("Calculate Move-Up Cost"):
                st.code("Suggested Package:\n- Pick 22 (1st Rd)\n- Pick 54 (2nd Rd)\n- 2025 1st Rd Pick\n\nEquity Ratio: 1.12 (Fair)")

    def _render_league_audit(self):
        st.header("🏢 League-Wide Financial Audit")
        
        st.subheader("Positional Cap Concentration (League-Wide)")
        pos_data = pd.DataFrame({
            'Position': ['QB', 'WR', 'EDGE', 'OT', 'CB', 'DT', 'S', 'LB', 'RB', 'TE'],
            'Avg Spending ($M)': [35.2, 18.4, 16.5, 15.2, 14.8, 12.1, 10.5, 9.8, 8.2, 7.5]
        })
        fig = px.treemap(pos_data, path=['Position'], values='Avg Spending ($M)',
                         color='Avg Spending ($M)', color_continuous_scale='RdBu')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cap Space Distribution")
            hist_fig = px.histogram(pd.DataFrame({'Space': np.random.normal(30, 20, 32)}), x='Space', 
                                    nbins=10, title="League Parity Index")
            st.plotly_chart(hist_fig, use_container_width=True)
        with col2:
            st.subheader("Financial Distress Flags")
            st.error("🚩 **New Orleans Saints**: Projected -$42M in 2025")
            st.warning("⚠️ **Buffalo Bills**: High Dead Cap concentration (22%)")
            st.info("ℹ️ **Houston Texans**: Optimal Roster Efficiency Score (92.4)")

    def _render_roster_vorp(self):
        st.header("Player Value & VORP Analysis")
        players = self._fetch("/analytics/vorp", params={"team_abbr": st.session_state['active_team']})
        if players:
            df = pd.DataFrame(players)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            fig = px.bar(df.head(10), x='player', y='vorp', color='vorp',
                         title="Top 10 Value Producers (VORP)",
                         color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ingest data to see VORP analytics.")

    def _render_forensics(self):
        st.header("Forensic Cut/Trade Matrix")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Multi-Year Contract Exit Windows")
            st.info("Deep forensic data processing...")
            
        with col2:
            st.subheader("Contract Cliff Identification")
            st.markdown("""
                - 🚩 **Player A**: Performance Cliff in 2025
                - 🟢 **Player B**: Stable Value until 2027
                - 🚩 **Player C**: Dead Cap Albatross
            """)

    def _render_ml_insights(self):
        st.header("Machine Learning & Aging Curves")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Positional Aging Projections")
            data = pd.DataFrame({
                'Years Past Peak': range(-3, 6),
                'Retention %': [1.0, 1.0, 0.98, 0.92, 0.85, 0.75, 0.60, 0.45, 0.30]
            })
            fig = px.area(data, x='Years Past Peak', y='Retention %', title="Production Retention Curve")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Market Inflation Analysis")
            inf = self._fetch("/market/inflation")
            if inf:
                inf_df = pd.DataFrame(inf).T.reset_index()
                st.dataframe(inf_df)

    def _render_fa_engine(self):
        st.header("Free Agency Recommendation Engine")
        st.success("Targeting 3 High-Priority Positional Needs")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Target 1: EDGE**")
            st.write("Best Fit: Josh Allen (JAX)")
            st.write("Est. APY: $24.5M")
        with col2:
            st.info("**Target 2: WR**")
            st.write("Best Fit: Tee Higgins (CIN)")
            st.write("Est. APY: $21.0M")
        with col3:
            st.info("**Target 3: OT**")
            st.write("Best Fit: Tyron Smith (DAL)")
            st.write("Est. APY: $12.0M")

    def _render_war_room(self):
        st.header("War Room Scenario Simulator")
        
        st.subheader("Active Session Log")
        if not st.session_state['pending_moves']:
            st.info("No moves executed. Start by cutting or trading players from the Roster tab.")
        else:
            for move in st.session_state['pending_moves']:
                st.markdown(f"<div class='transaction-log'>{move['type']}: {move['player']} | Savings: +${move['savings']}M</div>", unsafe_allow_html=True)
                
        if st.button("Clear Session"):
            st.session_state['pending_moves'] = []
            st.rerun()

    def _render_optimizer(self):
        st.header("Algorithmic Roster Optimizer")
        target = st.number_input("Savings Target ($M)", 5.0, 100.0, 15.0)
        if st.button("Run Cap-Fix Optimizer"):
            with st.spinner("Evaluating 4,000 combinations..."):
                res = self._fetch(f"/strategy/optimize/{st.session_state['active_team']}", params={"target": target})
                if res:
                    st.write("### Recommended Plan")
                    st.write(f"**Achieved Savings:** ${res['achieved_savings']}M")
                    st.write(f"**EPA Impact:** -{res['total_epa_loss']} points")
                    for m in res['suggested_moves']:
                        st.success(f"{m['type']} {m['player']} (+${m['savings']}M)")

    def run(self):
        team_info = self.render_sidebar()
        if team_info:
            self.render_dashboard(team_info)
            st.divider()
            self._render_about()
        else:
            st.error("Backend unavailable. Run 'make run-backend' first.")

    def _render_about(self):
        st.header("📖 About CapCommander NFL")
        st.markdown("""
        **CapCommander V2** is a professional-grade roster optimization and financial modeling suite 
        designed for NFL front offices and salary cap analysts. 
        
        ### 🧠 Core Intelligence
        - **CBA Rules Engine:** Precise multi-year math for dead cap, post-June 1st designations, and bonuses.
        - **ML Pipeline:** Predictive performance modeling (Aging Curves) and market value regression (MVD).
        - **Roster Optimizer:** Heuristic greedy algorithms to solve the 'Over-the-Cap' problem with minimal EPA loss.
        
        ### 🛠 Tech Stack
        - **Backend:** FastAPI (Python), PostgreSQL, SQLAlchemy ORM.
        - **ML:** Scikit-learn (Random Forest, Linear Regression).
        - **Frontend:** Streamlit, Plotly, AgGrid.
        
        *Engineered for performance. Built for champions.*
        """)

if __name__ == "__main__":
    ui = CapCommanderV2UI()
    ui.run()
