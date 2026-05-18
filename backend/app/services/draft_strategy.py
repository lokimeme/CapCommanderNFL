from typing import List, Dict, Optional, Tuple
from backend.app.services.draft_modeling import DraftValueCharts
import logging

logger = logging.getLogger("CapCommanderDraftStrategy")

class DraftStrategyService:

    @staticmethod
    def calculate_trade_up_cost(target_pick: int, team_picks: List[int], chart_type: str = "JJ") -> Dict:
        chart_func = DraftValueCharts.get_jimmy_johnson_value if chart_type == "JJ" else DraftValueCharts.get_chase_stuart_value
        
        target_value = chart_func(target_pick)
        
        sorted_picks = sorted(team_picks, key=lambda p: chart_func(p), reverse=True)
        
        selected_picks = []
        current_value = 0
        
        for p in sorted_picks:
            val = chart_func(p)
            if current_value + val <= target_value * 1.1:
                selected_picks.append(p)
                current_value += val
            
            if current_value >= target_value:
                break
                
        return {
            "target_pick": target_pick,
            "required_value": target_value,
            "suggested_package": selected_picks,
            "package_value": round(current_value, 2),
            "premium_paid": round(current_value - target_value, 2),
            "is_feasible": current_value >= target_value
        }

    @staticmethod
    def suggest_trade_down_scenarios(current_pick: int, chart_type: str = "JJ") -> List[Dict]:
        chart_func = DraftValueCharts.get_jimmy_johnson_value if chart_type == "JJ" else DraftValueCharts.get_chase_stuart_value
        current_val = chart_func(current_pick)
        
        scenarios = [
            {
                "name": "Mid-Round Slide",
                "picks": [current_pick + 15, current_pick + 35],
                "description": "Drop ~15 slots to pick up an early Day 2 selection."
            },
            {
                "name": "Exit Round",
                "picks": [current_pick + 32, current_pick + 45, current_pick + 64],
                "description": "Exit current round for multiple high Day 2/3 selections."
            },
            {
                "name": "Pick Accumulation",
                "picks": [current_pick + 5, current_pick + 64, current_pick + 96],
                "description": "Small slide to add depth in the middle rounds."
            }
        ]
        
        results = []
        for sc in scenarios:
            sc_val = sum(chart_func(p) for p in sc['picks'])
            results.append({
                "scenario_name": sc['name'],
                "projected_picks": sc['picks'],
                "total_value": round(sc_val, 2),
                "value_delta": round(sc_val - current_val, 2),
                "equity_ratio": round(sc_val / current_val, 2),
                "description": sc['description']
            })
            
        return sorted(results, key=lambda x: x['equity_ratio'], reverse=True)

    @staticmethod
    def analyze_pick_value_distribution(picks: List[int], chart_type: str = "JJ") -> Dict:
        chart_func = DraftValueCharts.get_jimmy_johnson_value if chart_type == "JJ" else DraftValueCharts.get_chase_stuart_value
        
        total_value = sum(chart_func(p) for p in picks)
        if total_value == 0: return {}
        
        round_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        
        for p in picks:
            if p <= 32: r = 1
            elif p <= 64: r = 2
            elif p <= 100: r = 3
            elif p <= 135: r = 4
            elif p <= 170: r = 5
            elif p <= 210: r = 6
            else: r = 7
            
            round_distribution[r] += chart_func(p)
            
        concentration = (round_distribution[1] + round_distribution[2]) / total_value
        
        strategy = "Balanced"
        if concentration > 0.75: strategy = "Star-Focused (High Risk/High Reward)"
        elif concentration < 0.4: strategy = "Volume-Focused (Draft & Develop)"
        
        return {
            "total_capital": round(total_value, 2),
            "round_distribution": round_distribution,
            "capital_concentration": round(concentration, 2),
            "draft_identity": strategy
        }

    @staticmethod
    def estimate_pro_bowl_probability(pick_number: int) -> float:
        if pick_number == 1: return 0.75
        
        prob = 0.8 * (pick_number ** -0.6)
        return round(max(0.01, min(0.75, prob)), 3)
