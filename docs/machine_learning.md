# Machine Learning & Predictive Analytics in CapCommander

This document details the ML models used to provide 'Market Intelligence' for front offices.

## 1. The Aging Curve Model
A Random Forest Regressor predicts a player's production (EPA) for the next 12-36 months.

### 1.1 Feature Selection
*   **Age:** The primary predictor.
*   **Positional Class:** RBs decay earliest, QBs latest.
*   **Historical Usage:** Cumulative snaps played.
*   **Efficiency Trends:** YoY change in EPA per snap.

### 1.2 Identifying 'The Cliff'
The model flags players who are within 1 season of their predicted 'Performance Cliff' (a 20%+ drop in production).

## 2. The Albatross Index (MVD)
Uses Linear Regression to establish a 'Market Fair Value' for every tier of production.

### 2.1 Positional Scarcity Weighting
Premium positions (QB, EDGE, LT, CB) receive a 1.2x to 1.5x multiplier on their Expected Points Added (EPA) before the regression is run. This reflects the 'Premium' teams pay for high-leverage talent.

### 2.2 Market Value Delta (MVD)
`MVD = Actual Cap Hit - Predicted Market Value`
*   **Negative MVD:** High-value bargains.
*   **Positive MVD:** Low-value albatrosses.

## 3. Injury Risk Simulation
A probabilistic model assesses the financial risk of a player's contract guarantees.

### 3.1 Historical Fragility
Players with < 10 games played in consecutive years receive a 15% risk premium.

### 3.2 Positional Baseline
Certain positions (e.g., RB) feature a higher baseline injury risk (35%) than others (e.g., QB, 15%).
