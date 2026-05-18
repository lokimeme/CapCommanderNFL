from typing import List, Dict
from backend.app.services.historical_analysis import HistoricalCapBenchmarks

class TeamNeedsService:
    
    @staticmethod
    def calculate_positional_needs(team_roster_stats: List[Dict]) -> Dict:
        allocation = HistoricalCapBenchmarks.analyze_roster_allocation(team_roster_stats)
        
        needs = {}
        for pos_group, stats in allocation.items():
            is_under_invested = stats['status'] == "Under-Invested"
            
            group_epa = sum(p['total_epa'] for p in team_roster_stats if p['position'] == pos_group)
            is_low_production = group_epa < 10.0
            
            priority = "Low"
            if is_under_invested and is_low_production: priority = "Critical"
            elif is_under_invested or is_low_production: priority = "Moderate"
            
            needs[pos_group] = {
                "priority": priority,
                "allocation_status": stats['status'],
                "group_epa": round(group_epa, 1)
            }
            
        return needs

    @staticmethod
    def evaluate_trade_strategic_fit(team_abbr: str, needs: Dict, incoming_player: Dict, outgoing_player: Dict = None) -> Dict:
        pos = incoming_player['position']
        mapping = {"OT": "OL", "DE": "DL", "EDGE": "DL", "CB": "DB", "S": "DB"}
        group = mapping.get(pos, pos)
        
        need_level = needs.get(group, {}).get("priority", "Low")
        
        score = 50
        if need_level == "Critical": score += 40
        elif need_level == "Moderate": score += 20
        
        if needs.get(group, {}).get("allocation_status") == "Over-Invested":
            score -= 20
            
        return {
            "strategic_score": min(100, max(0, score)),
            "verdict": "Strong Fit" if score > 70 else "Questionable" if score < 40 else "Neutral",
            "reasoning": f"Team has {need_level} need at {group}."
        }
