# Roster Optimization & Cap Management Guide

This document explains the algorithms used to fix a team's financial health in CapCommander.

## 1. The Greedy Optimization Algorithm
The Roster Optimizer uses a heuristic search to solve the 'Over-the-Cap' problem.

### 1.1 Efficiency Scoring
Every potential move is assigned an **Efficiency Score**:
`Efficiency = Savings Achieved / EPA Production Lost`
*   **Restructures:** Have an efficiency of +∞ because they clear space without any production loss.
*   **Cuts:** Efficiency varies based on the player's performance tier.

### 1.2 Constraint Solving
The algorithm iterates through sorted moves until:
1.  The target savings is reached.
2.  Positional minimums (e.g., 2 QBs, 8 OL) are threatened.
3.  The maximum move limit is reached.

## 2. Restructure Priority Matrix
Candidates for restructuring are prioritized based on:
*   **Base Salary:** High salaries provide the most 'Convertible Cash'.
*   **Future Utility:** Only players with high predicted 'Aging Curve' stability should be restructured (to avoid dead cap in later years).
*   **Contract Length:** More years remaining allows for better amortization of the signing bonus.

## 3. Identifying 'Dead Weight'
A player is flagged as 'Dead Weight' if they meet two criteria:
1.  **Low Efficiency:** Production (EPA) is in the bottom 25% of the position.
2.  **High Potential Savings:** Releasing them clears > $3M in space.

## 4. Multi-Year Planning (The 3-Year Window)
Optimization is never about just one year.
*   **Post-June 1st Cuts:** Used strategically to defer dead cap to 'The Next Year', opening up immediate room for Free Agency.
*   **Void Year Injection:** Adds dummy years to a contract to maximize proration, but at the cost of 'Cap Purgatory' in future seasons.
