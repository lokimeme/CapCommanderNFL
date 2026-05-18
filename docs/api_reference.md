# API Reference Guide

## 1. Teams API
Endpoints for retrieving NFL team information.

### `GET /teams/`
Returns a list of all 32 NFL teams.
- **Parameters:** `skip` (int), `limit` (int)
- **Response:** List of `Team` objects.

### `GET /teams/{team_abbr}`
Returns details for a specific team.
- **Response:** `Team` object.

## 2. Players API
Endpoints for player roster management.

### `GET /players/`
Returns a list of players, optionally filtered by team.
- **Parameters:** `team_abbr` (str), `skip` (int), `limit` (int)
- **Response:** List of `Player` objects.

### `GET /players/{gsis_id}`
Returns details for a specific player, including their team info.
- **Response:** `Player` object.

## 3. Contracts API
Endpoints for financial data.

### `GET /contracts/`
Returns contract summaries.
- **Parameters:** `team_abbr` (str), `player_id` (str)
- **Response:** List of `Contract` objects with nested `ContractYears`.

### `GET /contracts/{player_id}`
Returns the full multi-year contract for a specific player.
- **Response:** `Contract` object.

## 4. Stats API
Endpoints for performance data.

### `GET /stats/`
Returns seasonal stats for players.
- **Parameters:** `player_id` (str), `season` (int)
- **Response:** List of `SeasonalStats` objects.

### `GET /stats/top-epa`
Returns the top performers by Total EPA for a given season.
- **Parameters:** `limit` (int), `season` (int)
- **Response:** List of `SeasonalStats` objects.

## 5. Decision Modeling (Service Layer)
These are handled via internal services but can be exposed as RPC-style endpoints.

### `POST /forensics/cut-impact` (Planned)
Calculates Pre/Post-June 1st cut impact for a contract.

### `POST /trade/evaluate` (Planned)
Calculates financial deltas for a proposed player trade.
