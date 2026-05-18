# NFL Collective Bargaining Agreement (CBA) Rules Reference

This document outlines the specific financial mechanisms of the NFL CBA that are implemented (or planned) in the CapCommander Enterprise Suite.

## 1. Salary Cap Fundamentals
The NFL operates under a "hard" salary cap. Every dollar paid to a player must be accounted for against the team's cap for a specific year.

### 1.1 Minimum Salaries
The CBA mandates minimum salaries based on "Credited Seasons." For 2024, the rookie minimum is $795,000.

### 1.2 The "Top 51" Rule
During the offseason (from the start of the League Year until the first game), only the top 51 highest-paid players count against the cap. This allows teams to carry larger rosters for training camp.

## 2. Bonus Proration
Bonuses are handled differently than base salaries.

### 2.1 Signing Bonuses
Signing bonuses are paid upfront but prorated over the length of the contract (up to a maximum of 5 years).
*   **Example:** A $10M signing bonus on a 5-year deal counts as $2M/year against the cap.

### 2.2 Roster Bonuses
Usually paid on a specific date (e.g., the 5th day of the League Year). These are NOT prorated and count fully in the year they are paid.

### 2.3 Option Bonuses
Function similarly to signing bonuses and are prorated over the remaining years of the deal.

## 3. The Dead Cap Matrix
Dead cap occurs when a player is removed from the roster (via cut or trade) but still has unamortized bonuses on the books.

### 3.1 Pre-June 1st Designations
If a player is cut before June 1st, all future prorated bonuses "accelerate" to the current year's cap.
*   **Formula:** `Current Year Proration + All Future Year Prorations = Total Dead Cap`.

### 3.2 Post-June 1st Designations
Teams can designate up to two players per year as Post-June 1st cuts.
*   **Immediate Impact:** Only the current year's proration hits the cap now.
*   **Future Impact:** All future years' proration hits the NEXT year's cap.
*   **Wait Period:** The team does not receive the cap savings until June 2nd.

## 4. Special Designations

### 4.1 The Franchise Tag
A one-year contract that keeps a player from entering free agency.
*   **Exclusive Tag:** The average of the top 5 salaries at the position for the current year.
*   **Non-Exclusive Tag:** The average of the top 5 salaries at the position over the last 5 years.

### 4.2 5th Year Options
First-round picks have a team option for a 5th year on their rookie contract.
*   **Value:** Determined by performance (Pro Bowls, playtime) and slotted based on position.

### 4.3 Compensatory Picks
Awarded to teams that lose more "qualifying" free agents than they sign.
*   **Value:** Picks are awarded at the end of rounds 3 through 7.
*   **Formula:** Proprietary NFL formula based on salary, playtime, and postseason awards.
