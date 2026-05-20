# 🏈 CapCommander NFL: Enterprise Roster Forensic Suite (V2)

CapCommander is a high-performance, enterprise-grade NFL salary cap analysis and roster optimization engine. It is designed to provide "Front Office" level insights by merging real-time contract data, advanced on-field performance metrics, and machine learning.

---

## 🚀 Vision: The Enterprise War Room
Evolving from a prototype to a full-scale financial modeling engine, CapCommander V2 provides a robust, stateful environment for multi-year roster construction, predictive modeling, and rigorous CBA compliance.

### 🏛 Architecture
*   **Backend:** FastAPI (Python) - High-performance, typed REST API.
*   **Database:** SQLite (SQLAlchemy) - Managed via SQLAlchemy ORM for complex relational data.
*   **Intelligence:** Scikit-learn / XGBoost - Predictive modeling for performance and valuation.
*   **Interface:** Streamlit - Interactive dashboard and simulator.

---

## 🏗 Roadmap: The Path to 5,000+ LOC

### Phase 1: Architectural Overhaul (Foundation)
*   [x] **Database Migration:** SQLAlchemy models for Teams, Players, Contracts, Draft Picks, and Stats.
*   [x] **FastAPI Backend:** RESTful endpoints for stateful data access.
*   [x] **ETL Pipeline:** Robust data ingestion and transformation from `nfl_data_py`.

### Phase 2: The CBA Rules Engine (Core Logic)
*   [x] **Contract Logic:** Precise handling of Guaranteed Money, Signing vs. Roster Bonuses, and Post-June 1st designations.
*   [x] **Roster Status:** Practice Squad, IR, and 53-man roster limit tracking.
*   [x] **Advanced Mechanics:** Franchise Tags, 5th-Year Options, and Compensatory Pick formulas.

### Phase 3: Advanced Data Science & Machine Learning
*   [x] **Predictive Modeling:** The "Aging Curve" model for performance decline.
*   [x] **Injury Risk Assessment:** Probabilistic models for contract guarantee safety.
*   [x] **Market Value Delta (MVD):** ML-driven valuation comparisons against league benchmarks.

### Phase 4: Complex Feature Suites (The War Room)
*   [x] **Multi-Team Trade Machine:** 3+ team trade simulation with salary retention and cap absorption logic.
*   [x] **Mock Offseason Simulator:** Stateful free agency and draft simulation.
*   [x] **Historical Cap Analysis:** Visualizing championship roster allocation patterns.

---

## 🛠 Tech Stack
*   **Languages:** Python 3.12+
*   **Frameworks:** FastAPI, Streamlit
*   **Data:** SQLite, SQLAlchemy, DuckDB (for analytical caching)
*   **ML:** Scikit-learn, Pandas, NumPy
*   **Data Sources:** `nfl_data_py` (OverTheCap, NFL API)
