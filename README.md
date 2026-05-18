# 🏈 CapCommander NFL: Enterprise Roster Forensic Suite (V2)

CapCommander is a high-performance, enterprise-grade NFL salary cap analysis and roster optimization engine. It is designed to provide "Front Office" level insights by merging real-time contract data, advanced on-field performance metrics, and machine learning.

---

## 🚀 Vision: The Enterprise War Room
Evolving from a prototype to a full-scale financial modeling engine, CapCommander V2 provides a robust, stateful environment for multi-year roster construction, predictive modeling, and rigorous CBA compliance.

### 🏛 Architecture
*   **Backend:** FastAPI (Python) - High-performance, typed REST API.
*   **Database:** PostgreSQL - Managed via SQLAlchemy ORM for complex relational data.
*   **Intelligence:** Scikit-learn / XGBoost - Predictive modeling for performance and valuation.
*   **Interface:** Streamlit (Transitioning to a dedicated frontend) - Interactive dashboard and simulator.

---

## 🏗 Roadmap: The Path to 5,000+ LOC

### Phase 1: Architectural Overhaul (Foundation)
*   [ ] **Database Migration:** SQLAlchemy models for Teams, Players, Contracts, Draft Picks, and Stats.
*   [ ] **FastAPI Backend:** RESTful endpoints for stateful data access.
*   [ ] **ETL Pipeline:** Robust data ingestion and transformation from `nfl_data_py`.

### Phase 2: The CBA Rules Engine (Core Logic)
*   [ ] **Contract Logic:** Precise handling of Guaranteed Money, Signing vs. Roster Bonuses, and Post-June 1st designations.
*   [ ] **Roster Status:** Practice Squad, IR, and 53-man roster limit tracking.
*   [ ] **Advanced Mechanics:** Franchise Tags, 5th-Year Options, and Compensatory Pick formulas.

### Phase 3: Advanced Data Science & Machine Learning
*   [ ] **Predictive Modeling:** The "Aging Curve" model for performance decline.
*   [ ] **Injury Risk Assessment:** Probabilistic models for contract guarantee safety.
*   [ ] **Market Value Delta (MVD):** ML-driven valuation comparisons against league benchmarks.

### Phase 4: Complex Feature Suites (The War Room)
*   [ ] **Multi-Team Trade Machine:** 3+ team trade simulation with salary retention and cap absorption logic.
*   [ ] **Mock Offseason Simulator:** Stateful free agency and draft simulation.
*   [ ] **Historical Cap Analysis:** Visualizing championship roster allocation patterns.

---

## 🛠 Tech Stack
*   **Languages:** Python 3.10+
*   **Frameworks:** FastAPI, Streamlit
*   **Data:** PostgreSQL, SQLAlchemy, DuckDB (for analytical caching)
*   **ML:** Scikit-learn, Pandas, NumPy
*   **Data Sources:** `nfl_data_py` (OverTheCap, NFL API)
