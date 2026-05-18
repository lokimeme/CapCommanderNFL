import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("CapCommanderAnalytics")

class AdvancedMetricsEngine:

    @staticmethod
    def calculate_positional_replacement_level(all_players_stats: List[Dict]) -> Dict:
        df = pd.DataFrame(all_players_stats)
        if df.empty:
            return {}

        replacement_levels = {}
        for pos in df['position'].unique():
            pos_df = df[df['position'] == pos].sort_values(by='total_epa', ascending=False)
            
            n = len(pos_df)
            if n < 5:
                replacement_levels[pos] = pos_df['total_epa'].mean() * 0.5
                continue
                
            start_idx = int(n * 0.6)
            end_idx = int(n * 0.8)
            
            replacement_val = pos_df.iloc[start_idx:end_idx]['total_epa'].mean()
            replacement_levels[pos] = round(replacement_val, 2)

        return replacement_levels

    @staticmethod
    def calculate_vorp(player_stats: Dict, replacement_levels: Dict) -> float:
        pos = player_stats.get('position')
        total_epa = player_stats.get('total_epa', 0.0)
        
        replacement_val = replacement_levels.get(pos, 0.0)
        vorp = total_epa - replacement_val
        
        return round(vorp, 2)

    @staticmethod
    def calculate_efficiency_index(cap_hit: float, total_epa: float) -> float:
        if cap_hit <= 0.75:
            cap_hit = 0.75
            
        efficiency = (total_epa / cap_hit)
        return round(efficiency, 3)

    @staticmethod
    def identify_value_outliers(all_players: List[Dict], percentile: float = 90.0) -> Dict:
        df = pd.DataFrame(all_players)
        if df.empty:
            return {"bargains": [], "albatrosses": []}

        df['eff'] = df.apply(lambda r: (r['total_epa'] / max(r['cap_hit'], 0.75)), axis=1)
        
        bargains = []
        albatrosses = []
        
        for pos in df['position'].unique():
            pos_df = df[df['position'] == pos]
            if len(pos_df) < 5: continue
            
            upper_threshold = np.percentile(pos_df['eff'], percentile)
            lower_threshold = np.percentile(pos_df['eff'], 100 - percentile)
            
            pos_bargains = pos_df[pos_df['eff'] >= upper_threshold]
            pos_albatrosses = pos_df[pos_df['eff'] <= lower_threshold]
            
            bargains.extend(pos_bargains.to_dict('records'))
            albatrosses.extend(pos_albatrosses.to_dict('records'))
            
        return {
            "bargains": bargains,
            "albatrosses": albatrosses
        }

    @staticmethod
    def calculate_roster_health_score(roster_stats: List[Dict], positional_needs: Dict) -> float:
        if not roster_stats: return 0.0
        
        total_epa = sum(p.get('total_epa', 0.0) for p in roster_stats)
        
        penalty = 0
        for pos_group, need in positional_needs.items():
            if need['priority'] == "Critical" and need['group_epa'] <= 0:
                penalty += 15
                
        base_score = min(100, (total_epa / 150) * 100)
        
        final_score = max(0, base_score - penalty)
        return round(final_score, 1)
