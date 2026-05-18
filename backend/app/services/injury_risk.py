from typing import Dict, List, Optional

class InjuryRiskModel:
    POSITIONAL_RISK_BASE = {
        "RB": 0.35, "WR": 0.28, "TE": 0.25, "QB": 0.15,
        "OL": 0.22, "DL": 0.24, "LB": 0.30, "CB": 0.26, "S": 0.27
    }

    @classmethod
    def calculate_risk_score(cls, position: str, age: int, games_played_last_year: int) -> Dict:
        base_risk = cls.POSITIONAL_RISK_BASE.get(position, 0.20)
        age_factor = max(0, (age - 27) * 0.02)
        usage_factor = 0
        if games_played_last_year < 10:
            usage_factor = 0.10
        elif games_played_last_year == 17:
            usage_factor = -0.05
        final_risk = min(0.95, base_risk + age_factor + usage_factor)
        safety_score = 100 * (1 - final_risk)
        verdict = "Low Risk"
        if final_risk > 0.50: verdict = "High Risk"
        elif final_risk > 0.30: verdict = "Moderate Risk"
        return {
            "risk_percentage": round(final_risk * 100, 1),
            "safety_score": round(safety_score, 1),
            "verdict": verdict,
            "positional_baseline": base_risk * 100
        }

    @classmethod
    def get_financial_exposure(cls, risk_score: float, guaranteed_salary: float) -> float:
        return round(guaranteed_salary * (risk_score / 100), 2)
