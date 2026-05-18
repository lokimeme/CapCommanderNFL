import pandas as pd
from typing import List, Dict, Optional, Tuple
from backend.app.services.cba_rules import calculate_detailed_cut_impact
from backend.app.services.models.restructure import simulate_simple_restructure
import logging

logger = logging.getLogger("CapCommanderOptimizer")

class RosterOptimizer:
    @staticmethod
    def find_optimal_cap_fixes(roster_data: List[Dict], target_savings: float, current_year: int = 2024, max_moves: int = 5) -> Dict:
        if target_savings <= 0: return {"message": "Team compliant.", "suggested_moves": []}
        potential_moves = []
        for p in roster_data:
            cut_impact = calculate_detailed_cut_impact(p['contract_obj'], current_year)
            if cut_impact and cut_impact['pre_june_1']['savings'] > 0:
                potential_moves.append({
                    "player": p['name'], "type": "CUT", "savings": cut_impact['pre_june_1']['savings'],
                    "epa_loss": p['total_epa'], "efficiency": cut_impact['pre_june_1']['savings'] / (p['total_epa'] + 0.1) 
                })
            res_impact = simulate_simple_restructure(p['cap_hit'], p['base_salary'], 0, years_remaining=3)
            if res_impact['savings'] > 0:
                potential_moves.append({
                    "player": p['name'], "type": "RESTRUCTURE", "savings": res_impact['savings'],
                    "epa_loss": 0.0, "efficiency": 9999.0
                })
        sorted_moves = sorted(potential_moves, key=lambda x: x['efficiency'], reverse=True)
        selected_moves, accumulated_savings, total_epa_loss = [], 0.0, 0.0
        for move in sorted_moves:
            if accumulated_savings >= target_savings or len(selected_moves) >= max_moves: break
            selected_moves.append(move)
            accumulated_savings += move['savings']
            total_epa_loss += move['epa_loss']
        return {
            "target_savings": round(target_savings, 2), "achieved_savings": round(accumulated_savings, 2),
            "total_epa_loss": round(total_epa_loss, 2), "is_target_met": accumulated_savings >= target_savings,
            "suggested_moves": selected_moves
        }

    @staticmethod
    def analyze_restructure_candidates(roster_data: List[Dict]) -> List[Dict]:
        candidates = []
        for p in roster_data:
            if p['base_salary'] > 5.0:
                score = (p['base_salary'] * 0.6) + (p['total_epa'] * 0.4)
                candidates.append({
                    "player": p['name'], "base_salary": p['base_salary'], "epa": p['total_epa'],
                    "restructure_priority_score": round(score, 2)
                })
        return sorted(candidates, key=lambda x: x['restructure_priority_score'], reverse=True)

    @staticmethod
    def identify_dead_weight(roster_data: List[Dict], current_year: int) -> List[Dict]:
        candidates = []
        for p in roster_data:
            cut_impact = calculate_detailed_cut_impact(p['contract_obj'], current_year)
            if not cut_impact: continue
            savings = cut_impact['pre_june_1']['savings']
            epa = p['total_epa']
            if epa < 5.0 and savings > 2.0:
                candidates.append({
                    "player": p['name'], "savings_if_cut": round(savings, 2), "current_epa": round(epa, 2),
                    "efficiency_ratio": round(savings / (epa + 0.1), 2)
                })
        return sorted(candidates, key=lambda x: x['efficiency_ratio'], reverse=True)

    @staticmethod
    def generate_optimization_strategy(team_abbr: str, roster_stats: List[Dict], target: float) -> str:
        opt_results = RosterOptimizer.find_optimal_cap_fixes(roster_stats, target)
        lines = [f"📈 CAP OPTIMIZATION STRATEGY: {team_abbr}", "=" * 40]
        lines.append(f"Target Savings: ${target}M")
        lines.append(f"Suggested Savings: ${opt_results['achieved_savings']}M")
        lines.append(f"Projected EPA Impact: -{opt_results['total_epa_loss']} pts")
        lines.append("\nRECOMMENDED ACTION PLAN:")
        for i, move in enumerate(opt_results['suggested_moves'], 1):
            lines.append(f" {i}. {move['type']} {move['player']} (+${move['savings']:.1f}M)")
        if not opt_results['is_target_met']: lines.append("\n🚨 WARNING: Savings goal not met.")
        else: lines.append("\n✅ SUCCESS: Goal achieved.")
        return "\n".join(lines)
