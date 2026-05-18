import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from backend.app.services.team_needs import TeamNeedsService
from backend.app.services.ml_engine import calculate_mvd_albatross
import logging

logger = logging.getLogger("CapCommanderFreeAgency")

class FreeAgencyRecommendationEngine:

    @staticmethod
    def identify_target_free_agents(
        team_needs: Dict, 
        available_fas: List[Dict], 
        max_budget: float
    ) -> List[Dict]:
        targets = []
        
        priority_map = {"Critical": 3, "Moderate": 2, "Low": 1}
        sorted_needs = sorted(
            team_needs.items(), 
            key=lambda x: priority_map.get(x[1]['priority'], 0), 
            reverse=True
        )
        
        remaining_budget = max_budget
        
        for pos_group, need_info in sorted_needs:
            if need_info['priority'] == "Low": continue
            if remaining_budget <= 1.0: break
            
            pos_fas = [fa for fa in available_fas if fa['position'] == pos_group]
            
            pos_fas = sorted(pos_fas, key=lambda x: x.get('total_epa', 0.0), reverse=True)
            
            for fa in pos_fas:
                apy = fa.get('projected_apy', 5.0)
                if apy <= remaining_budget:
                    targets.append({
                        "player": fa['name'],
                        "position": fa['position'],
                        "priority_addressed": need_info['priority'],
                        "cost": apy,
                        "epa_gain": fa.get('total_epa', 0.0),
                        "value_score": fa.get('total_epa', 0.0) / apy
                    })
                    remaining_budget -= apy
                    break
                    
        return targets

    @staticmethod
    def calculate_budget_allocation(
        total_cap_space: float, 
        needs: Dict, 
        roster_count: int
    ) -> Dict:
        reserve = 15.0
        spendable = max(0, total_cap_space - reserve)
        
        critical_count = len([n for n in needs.values() if n['priority'] == "Critical"])
        moderate_count = len([n for n in needs.values() if n['priority'] == "Moderate"])
        
        total_units = (critical_count * 3) + (moderate_count * 1)
        if total_units == 0:
            return {"total_spendable": spendable, "allocation": {}}
            
        unit_value = spendable / total_units
        
        allocation = {}
        for pos, info in needs.items():
            if info['priority'] == "Critical":
                allocation[pos] = round(unit_value * 3, 2)
            elif info['priority'] == "Moderate":
                allocation[pos] = round(unit_value * 1, 2)
                
        return {
            "total_spendable": round(spendable, 2),
            "reserve_funds": reserve,
            "allocation_by_position": allocation,
            "strategy": "Aggressive" if critical_count < 3 else "Depth-Focused"
        }

    @staticmethod
    def predict_market_value(player_stats: Dict, league_averages: Dict) -> Dict:
        pos = player_stats.get('position')
        epa = player_stats.get('total_epa', 0.0)
        age = player_stats.get('age', 26)
        
        avg_cost_per_epa = league_averages.get(pos, 0.5)
        
        raw_val = epa * avg_cost_per_epa
        
        age_penalty = 1.0
        if age > 30:
            age_penalty = 1.0 - ((age - 30) * 0.15)
            
        premiums = {"QB": 1.4, "LT": 1.25, "EDGE": 1.3, "CB": 1.2}
        premium = premiums.get(pos, 1.0)
        
        predicted_apy = max(0.8, raw_val * age_penalty * premium)
        
        return {
            "predicted_apy": round(predicted_apy, 2),
            "production_value": round(raw_val, 2),
            "age_adjustment_factor": round(age_penalty, 2),
            "market_status": "Premium" if premium > 1.1 else "Standard"
        }

    @staticmethod
    def generate_fa_advisory_report(team_abbr: str, targets: List[Dict], allocation: Dict) -> str:
        lines = [f"🏈 FREE AGENCY STRATEGIC BRIEF: {team_abbr}", "=" * 40]
        lines.append(f"Total FA Budget: ${allocation['total_spendable']}M")
        lines.append(f"Roster Strategy: {allocation['strategy']}")
        
        lines.append("\nPOSITIONAL SPENDING GUIDELINES:")
        for pos, amt in allocation['allocation_by_position'].items():
            lines.append(f" - {pos}: Up to ${amt}M")
            
        lines.append("\nTOP EXTERNAL TARGETS:")
        for i, t in enumerate(targets, 1):
            lines.append(f" {i}. {t['player']} ({t['position']})")
            lines.append(f"    Est. Cost: ${t['cost']}M | EPA Gain: +{t['epa_gain']}")
            lines.append(f"    Strategic Fit: Matches {t['priority_addressed']} need.")
            
        return "\n".join(lines)
