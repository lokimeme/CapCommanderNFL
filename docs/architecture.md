# CapCommander V2 Architecture Design

## 1. System Overview
CapCommander V2 is built as a decoupled, service-oriented application. It separates the presentation layer (Streamlit) from the business logic and data access layers (FastAPI + SQLAlchemy).

## 2. Component Diagram

### 2.1 Backend (FastAPI)
The core of the system. It handles:
- **API Layer:** Typed endpoints using Pydantic for request/response validation.
- **Service Layer:** Business logic for trades, cuts, draft modeling, and ML.
- **Data Access Layer:** SQLAlchemy ORM abstraction for PostgreSQL/SQLite.

### 2.2 Frontend (Streamlit)
A stateful dashboard that consumes the backend API.
- **Session State:** Tracks pending "War Room" moves.
- **Visualization:** Interactive charts using Plotly and Altair.

### 2.3 Data Pipeline (ETL)
A robust ingestion suite that fetches data from `nfl_data_py` and populates the relational database.

## 3. Data Model Design

### 3.1 Teams & Players
Basic relational data identifying the entities in the NFL.

### 3.2 Contracts (The Core)
Contracts are modeled as a one-to-many relationship with `ContractYears`. This allows for precise tracking of changing cap hits, base salaries, and bonus proration.

### 3.3 Stats & Performance
Seasonal statistics are linked to players, allowing for production-to-cost analysis (EPA/$M).

## 4. Machine Learning Integration

### 4.1 Aging Curve Model
A Random Forest Regressor predicts future performance based on a player's age and position. This allows GMs to identify "The Cliff"—the point where a player's production is expected to drop off significantly.

### 4.2 Albatross Index (MVD)
Linear regression calculates the expected cap hit for a player given their EPA production. The delta between actual and expected cap hit identifies market inefficiencies.

## 5. Deployment Strategy

### 5.1 Containerization
The entire suite is containerized using Docker, with a `docker-compose.yml` defining the backend, frontend, and PostgreSQL services.

### 5.2 Scalability
The FastAPI backend can be scaled horizontally behind a load balancer. PostgreSQL provides ACID-compliant persistence for high-concurrency environments.
