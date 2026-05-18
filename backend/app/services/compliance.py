import logging
from typing import List, Dict, Optional

logger = logging.getLogger("CapCommanderCompliance")

class CBAComplianceEngine:

    ROSTER_LIMITS = {
        "active": 53,
        "gameday": 48,
        "practice_squad": 16,
        "top_51": 51
    }

    @staticmethod
    def check_roster_validity(roster: List[Dict]) -> Dict:
        total_players = len(roster)
        by_position = {}
        for p in roster:
            pos = p.get('position', 'Unknown')
            by_position[pos] = by_position.get(pos, 0) + 1
            
        warnings = []
        if total_players > CBAComplianceEngine.ROSTER_LIMITS["active"]:
            warnings.append(f"Exceeds Active Roster Limit: {total_players}/{CBAComplianceEngine.ROSTER_LIMITS['active']}")
        
        min_requirements = {
            "QB": 2, "RB": 3, "WR": 5, "TE": 3, "OL": 8,
            "DL": 6, "LB": 6, "CB": 5, "S": 4, "K": 1, "P": 1
        }
        
        for pos, req in min_requirements.items():
            count = by_position.get(pos, 0)
            if count < req:
                warnings.append(f"Positional Deficit: {pos} has {count} (Min: {req})")
                
        return {
            "is_valid": len(warnings) == 0,
            "total_count": total_players,
            "warnings": warnings,
            "position_breakdown": by_position
        }

    @staticmethod
    def calculate_ir_cap_relief(player_contract: Dict, games_on_ir: int) -> float:
        base_salary = player_contract.get('base_salary', 0.0)
        has_injury_split = player_contract.get('has_injury_split', False)
        
        if not has_injury_split:
            return 0.0
            
        reduction_per_game = (base_salary / 17) * 0.5
        relief = reduction_per_game * games_on_ir
        
        return round(relief, 2)

    @staticmethod
    def validate_practice_squad_eligibility(player: Dict) -> Dict:
        years_exp = player.get('years_exp', 0)
        accrued_seasons = player.get('accrued_seasons', 0)
        
        is_eligible = False
        limit_type = "None"
        
        if accrued_seasons < 3:
            is_eligible = True
            limit_type = "Standard"
        elif accrued_seasons >= 3:
            is_eligible = True
            limit_type = "Veteran (Max 6)"
            
        return {
            "player": player['name'],
            "is_eligible": is_eligible,
            "limit_category": limit_type,
            "accrued_seasons": accrued_seasons
        }

    @staticmethod
    def calculate_top_51_cap(roster_contracts: List[Dict]) -> float:
        all_hits = sorted([c['cap_number'] for c in roster_contracts], reverse=True)
        top_51 = all_hits[:CBAComplianceEngine.ROSTER_LIMITS["top_51"]]
        return round(sum(top_51), 2)
