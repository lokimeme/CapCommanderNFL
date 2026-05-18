import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("CapCommanderIncentives")

class CBAIncentiveService:

    @staticmethod
    def evaluate_incentive_status(player_previous_stats: Dict, incentive_criteria: Dict) -> str:
        metric = incentive_criteria.get("metric")
        threshold = incentive_criteria.get("threshold")
        
        previous_value = player_previous_stats.get(metric, 0)
        
        if previous_value >= threshold:
            return "LTBE"
        return "NLTBE"

    @staticmethod
    def calculate_cap_impact(incentives: List[Dict]) -> Dict:
        current_cap_charge = 0.0
        potential_deferred_charge = 0.0
        
        for inc in incentives:
            if inc['status'] == "LTBE":
                current_cap_charge += inc['value']
            else:
                potential_deferred_charge += inc['value']
                
        return {
            "immediate_charge": round(current_cap_charge, 2),
            "deferred_potential": round(potential_deferred_charge, 2)
        }

    @staticmethod
    def process_end_of_year_adjustments(actual_performance: Dict, contract_incentives: List[Dict]) -> Dict:
        adjustment_delta = 0.0
        details = []
        
        for inc in contract_incentives:
            metric = inc['metric']
            threshold = inc['threshold']
            value = inc['value']
            status = inc['status']
            
            actual_val = actual_performance.get(metric, 0)
            earned = actual_val >= threshold
            
            impact = 0.0
            if status == "LTBE":
                if not earned:
                    impact = value
                    details.append(f"LTBE Not Earned ({metric}): +${value}M Credit")
            else:
                if earned:
                    impact = -value
                    details.append(f"NLTBE Earned ({metric}): -${value}M Debit")
            
            adjustment_delta += impact
            
        return {
            "next_year_adjustment": round(adjustment_delta, 2),
            "adjustment_details": details
        }

    @staticmethod
    def simulate_incentive_scenarios(contract_incentives: List[Dict], scenarios: List[Dict]) -> List[Dict]:
        results = []
        for scenario in scenarios:
            adjustment = CBAIncentiveService.process_end_of_year_adjustments(
                scenario['stats'], 
                contract_incentives
            )
            results.append({
                "scenario_name": scenario['name'],
                "net_adjustment": adjustment['next_year_adjustment'],
                "details": adjustment['adjustment_details']
            })
            
        return results

    @staticmethod
    def validate_incentive_compliance(incentives: List[Dict], total_contract_value: float) -> List[str]:
        errors = []
        total_incentive_value = sum(i['value'] for i in incentives)
        
        if total_incentive_value > total_contract_value * 0.5:
            errors.append("WARNING: Total incentive value exceeds 50% of contract. May trigger league review.")
            
        for inc in incentives:
            if inc['value'] <= 0:
                errors.append(f"ERROR: Incentive '{inc['metric']}' has non-positive value.")
                
        return errors
