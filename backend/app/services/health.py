import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from backend.app.services.ml_engine import predict_performance_decline
import logging

logger = logging.getLogger("CapCommanderHealth")

class RosterHealthService:
    @staticmethod
    def calculate_resilience_grade(roster_data: List[Dict], current_year: int) -> Dict:
        ages = [p['age'] for p in roster_data]
        avg_age = np.mean(ages) if ages else 28
        age_score = 100 - (max(0, avg_age - 24) * 8)
        
        continuity_count = 0
        for p in roster_data:
            future_years = [y for y in p.get('contract_years', []) if y > current_year]
            if len(future_years) >= 2:
                continuity_count += 1
        
        continuity_pct = (continuity_count / len(roster_data)) if roster_data else 0
        continuity_score = continuity_pct * 100
        
        flexible_count = 0
        for p in roster_data:
            if p.get('max_potential_savings', 0) > 2.0:
                flexible_count += 1
                
        flex_score = (flexible_count / len(roster_data)) * 100 if roster_data else 0
        composite = (age_score * 0.4) + (continuity_score * 0.3) + (flex_score * 0.3)
        
        grade = "D"
        if composite >= 90: grade = "A+"
        elif composite >= 80: grade = "A"
        elif composite >= 70: grade = "B"
        elif composite >= 60: grade = "C"
        
        return {
            "resilience_score": round(composite, 1),
            "grade": grade,
            "sub_metrics": {
                "age_stability": round(age_score, 1),
                "continuity": round(continuity_score, 1),
                "flexibility": round(flex_score, 1)
            }
        }

    @staticmethod
    def identify_roster_fragility_points(roster_data: List[Dict]) -> List[Dict]:
        fragile_spots = []
        df = pd.DataFrame(roster_data)
        if df.empty: return []
        
        for pos in df['position'].unique():
            pos_df = df[df['position'] == pos]
            starters = pos_df.sort_values(by='total_epa', ascending=False).head(2)
            avg_starter_age = starters['age'].mean()
            depth = pos_df.sort_values(by='total_epa', ascending=False).iloc[2:]
            depth_continuity = len([p for p in depth.to_dict('records') if p.get('years_remaining', 0) > 1])
            
            if avg_starter_age > 30 and depth_continuity == 0:
                fragile_spots.append({
                    "position": pos,
                    "reason": "Aging starters with no established depth signed past this year.",
                    "severity": "High"
                })
        return fragile_spots

    @staticmethod
    def predict_roster_turnover(roster_data: List[Dict], year: int) -> Dict:
        turnover_count = 0
        for p in roster_data:
            if p.get('contract_end_year', 2024) <= year:
                turnover_count += 1
            elif p.get('is_cliff_candidate'):
                turnover_count += 1
        turnover_pct = (turnover_count / len(roster_data)) * 100 if roster_data else 0
        return {
            "target_year": year,
            "predicted_departures": turnover_count,
            "turnover_percentage": round(turnover_pct, 1),
            "roster_stability": "Stable" if turnover_pct < 30 else "High Volatility"
        }
