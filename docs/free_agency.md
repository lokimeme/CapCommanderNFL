# Free Agency Strategic Playbook

This document details the front-office principles used by the Free Agency Recommendation Engine in CapCommander.

## 1. Budget Segmentation
The 'War Chest' is never spent all at once. It is segmented into three buckets:

### 1.1 The Primary Target Pool (60% of Spendable)
Reserved for 1-2 'Difference Makers'—players with VORP > 20.0 and Tier 1 market value. 

### 1.2 Roster Stabilization (25% of Spendable)
Mid-tier veterans used to fill 'Moderate Needs'. Typically 2-3 year deals with flexible exit windows.

### 1.3 Depth & Special Teams (15% of Spendable)
One-year 'prove-it' deals and specialist contracts.

## 2. Market Value Prediction (MVP)
The AI predicts market value based on three key regressions:
1.  **Production-to-Cost:** The baseline $M per EPA point for the position.
2.  **Age Discount:** The historical decay of earnings after age 30.
3.  **Position Premium:** The scarcity-weighted multiplier (QB > WR > RB).

## 3. Positional Needs Integration
The system prioritizes targets using a 'Strategic Fit Score':
*   **Need Match:** Does the FA match a 'Critical' or 'Moderate' team deficit?
*   **Scheme Alignment:** Is the FA a technical fit for the team's historical EPA patterns?
*   **Roster Health Impact:** How much will this signing improve the team's overall health score?

## 4. Contract Structuring
Recommendations are made based on a team's '3-Year Window':
*   **Front-Loading:** Used when a team has significant current space and needs future flexibility.
*   **Back-Loading:** Used for 'All-In' windows where current cap hits are minimized via dummy void years.
