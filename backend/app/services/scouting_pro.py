import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import random
import logging

logger = logging.getLogger("CapCommanderScoutingPro")

class ProspectScoutingEngine:

    @staticmethod
    def calculate_prospect_grade(
        combine_stats: Dict, 
        game_tape_score: float, 
        production_metrics: Dict
    ) -> Dict:
        tape_weighted = game_tape_score * 0.6
        
        prod_score = (production_metrics.get('dominator_rating', 0.0) * 10) + \
                     (production_metrics.get('yards_per_route_run', 0.0) * 2)
        prod_weighted = min(10.0, prod_score) * 0.25
        
        ras = combine_stats.get('ras', 5.0)
        ras_weighted = ras * 0.15
        
        composite = tape_weighted + prod_weighted + ras_weighted
        
        tier = "Late Round"
        if composite >= 9.0: tier = "Generational Prospect"
        elif composite >= 8.0: tier = "Day 1 Starter"
        elif composite >= 7.0: tier = "High-End Developmental"
        elif composite >= 6.0: tier = "Rotation Depth"
        
        return {
            "composite_grade": round(composite, 2),
            "tier": tier,
            "sub_scores": {
                "tape": round(tape_weighted, 2),
                "production": round(prod_weighted, 2),
                "athleticism": round(ras_weighted, 2)
            }
        }

    @staticmethod
    def identify_draft_sleepers(all_prospects: List[Dict]) -> List[Dict]:
        sleepers = []
        for p in all_prospects:
            tape = p.get('game_tape_score', 0.0)
            ras = p.get('ras', 0.0)
            
            if tape > 8.0 and ras < 4.0:
                sleepers.append({
                    "name": p['name'],
                    "position": p['position'],
                    "reasoning": "Elite technical tape masked by sub-par testing numbers."
                })
            
            if p.get('is_small_school') and tape > 7.5:
                sleepers.append({
                    "name": p['name'],
                    "position": p['position'],
                    "reasoning": "Small school dominance; technical traits translate to NFL."
                })
                
        return sleepers

    @staticmethod
    def generate_draft_board(prospects: List[Dict], positional_needs: Dict) -> List[Dict]:
        board = []
        for p in prospects:
            base_grade = p.get('composite_grade', 5.0)
            
            need = positional_needs.get(p['position'], {}).get('priority', 'Low')
            multi = 1.0
            if need == "Critical": multi = 1.25
            elif need == "Moderate": multi = 1.1
            
            board.append({
                "name": p['name'],
                "position": p['position'],
                "adjusted_grade": round(base_grade * multi, 2),
                "rank": 0
            })
            
        board = sorted(board, key=lambda x: x['adjusted_grade'], reverse=True)
        for i, entry in enumerate(board, 1):
            entry['rank'] = i
            
        return board

    @staticmethod
    def simulate_mock_draft(board: List[Dict], team_slots: List[int]) -> List[Dict]:
        selections = []
        available = board.copy()
        
        for slot in sorted(team_slots):
            num_taken = slot - 1
            if len(available) > num_taken:
                player = available.pop(num_taken)
                selections.append({"pick": slot, "player": player['name'], "pos": player['position']})
                
        return selections
