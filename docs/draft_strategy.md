# NFL Draft Strategy & Scouting Guide

This guide outlines the methodologies used in CapCommander for draft pick valuation, prospect evaluation, and trade strategy.

## 1. Pick Valuation Models
CapCommander implements two primary models for valuing draft picks:

### 1.1 The Jimmy Johnson Chart (JJ)
The industry standard since the 1990s. It uses a 3,000-point scale for the #1 overall pick, decaying rapidly down to just a few points in the 7th round.
*   **Best Use:** Traditional trade-up/down scenarios.
*   **Criticism:** Overvalues top-of-the-draft picks relative to their actual on-field production.

### 1.2 The Chase Stuart Model (CS)
Based on historical Approximate Value (AV). It has a much flatter decay curve than the JJ chart.
*   **Best Use:** Teams focused on draft volume and 'roster depth'.
*   **Identity:** High correlation with 'Moneyball' style front offices.

## 2. Prospect Grading System
Prospects are graded on a scale of 0.0 to 10.0 based on three integrated pillars:

### 2.1 Game Tape (60% Weight)
The most subjective but critical component. Grades technical traits, scheme fit, and processing speed.

### 2.2 Production Metrics (25% Weight)
*   **Dominator Rating:** The percentage of a team's total production (yards/TDs) accounted for by the prospect.
*   **Breakout Age:** The age at which the prospect first achieved a 20%+ Dominator Rating.

### 2.3 Athletic Testing (15% Weight)
Uses the **Relative Athletic Score (RAS)**, which normalizes combine results (40-yard dash, vertical, etc.) by position on a 0-10 scale.

## 3. Draft Day Mechanisms

### 3.1 Trade-Up Feasibility
A team looking to move up must provide a package of picks with total value exceeding the target pick's value plus a 'Premium' (typically 10-20% for top-10 selections).

### 3.2 Trade-Down Equity
Trading down is modeled as a way to maximize total draft capital. A 'Successful' trade down is defined as one where the equity ratio (Value Received / Value Relinquished) is > 1.15.

## 4. The Rookie Wage Scale
Implemented since the 2011 CBA, the rookie wage scale slots every pick into a pre-determined 4-year contract.
*   **1st Round Picks:** Feature a 5th-year team option.
*   **2nd-7th Round:** Fixed 4-year deals with no option.
*   **Cap Charge:** Prorated signing bonus + league minimum base salary.
