from typing import List, Dict, Optional
import numpy as np
from backend.app.models.player import Player
from backend.app.services.analytics import AdvancedMetricsEngine
import logging

logger = logging.getLogger("CapCommanderScoutingAI")

class ScoutingAIService:

    @staticmethod
    def find_statistical_clones(player_stats: Dict, all_players_stats: List[Dict], top_n: int = 5) -> List[Dict]:
        target_epa = player_stats.get('total_epa', 0.0)
        target_age = player_stats.get('age', 26)
        
        clones = []
        for p in all_players_stats:
            if p['player_id'] == player_stats['player_id']: continue
            if p['position'] != player_stats['position']: continue
            
            distance = np.sqrt(
                (p['total_epa'] - target_epa)**2 + 
                ((p['age'] - target_age) * 10)**2
            )
            
            clones.append({
                "player": p['name'],
                "team": p['team_abbr'],
                "epa": p['total_epa'],
                "age": p['age'],
                "similarity_score": round(100 / (1 + distance), 1)
            })
            
        return sorted(clones, key=lambda x: x['similarity_score'], reverse=True)[:top_n]

    @staticmethod
    def recommend_contract_structure(player_profile: Dict, market_trends: Dict) -> Dict:
        age = player_profile.get('age', 26)
        pos = player_profile.get('position', 'WR')
        target_apy = player_profile.get('target_apy', 10.0)
        length = 4
        
        structure = []
        is_front_loaded = age <= 25
        
        total_val = target_apy * length
        signing_bonus = total_val * 0.3
        
        for i in range(1, length + 1):
            if is_front_loaded:
                multi = 1.2 if i == 1 else 1.0 if i == 2 else 0.9
            else:
                multi = 0.8 if i == 1 else 0.9 if i == 2 else 1.1 if i == 3 else 1.2
                
            base = (target_apy * multi) - (signing_bonus / length)
            
            structure.append({
                "year": 2024 + i - 1,
                "base_salary": round(base, 2),
                "signing_bonus_proration": round(signing_bonus / length, 2),
                "total_cap_hit": round(base + (signing_bonus/length), 2)
            })
            
        return {
            "recommended_strategy": "Front-Loaded" if is_front_loaded else "Back-Loaded (Incentive heavy)",
            "length": length,
            "total_value": round(total_val, 2),
            "apy": target_apy,
            "yearly_hits": structure
        }

    @staticmethod
    def identify_positional_market_leaders(contracts: List[Dict]) -> Dict:
        leaders = {}
        for c in contracts:
            pos = c['position']
            if pos not in leaders or c['avg_annual'] > leaders[pos]['apy']:
                leaders[pos] = {
                    "player": c['player'],
                    "apy": c['avg_annual'],
                    "total_guaranteed": c['total_guaranteed']
                }
        return leaders
