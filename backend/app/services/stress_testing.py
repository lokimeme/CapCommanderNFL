import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import random
import uuid
import logging

logger = logging.getLogger("CapCommanderStressTest")

class SyntheticDataGenerator:

    @staticmethod
    def generate_bulk_players(count: int = 1000) -> List[Dict]:
        positions = ['QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'C', 'DE', 'DT', 'LB', 'CB', 'S', 'K', 'P']
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        players = []
        for _ in range(count):
            players.append({
                "gsis_id": str(uuid.uuid4()),
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "position": random.choice(positions),
                "age": random.randint(21, 38),
                "years_exp": random.randint(0, 15),
                "team_abbr": random.choice(["KC", "CHI", "BUF", "DAL", "SF", "PHI", "CIN", "DET"])
            })
        return players

    @staticmethod
    def generate_bulk_contracts(players: List[Dict]) -> List[Dict]:
        contracts = []
        for p in players:
            base_val = 1.0
            if p['position'] == "QB": base_val = 25.0
            elif p['position'] in ["OT", "EDGE", "WR", "CB"]: base_val = 15.0
            
            age_mod = 1.0 - abs(p['age'] - 27) * 0.05
            val = max(1.0, base_val * age_mod * random.uniform(0.7, 1.3))
            
            length = random.randint(1, 5)
            year_signed = 2024 - random.randint(0, length - 1)
            
            years_data = []
            for i in range(length):
                curr_year = year_signed + i
                years_data.append({
                    "year": curr_year,
                    "cap_number": val * (1 + (i * 0.1)),
                    "base_salary": val * 0.7,
                    "signing_bonus": val * 0.2,
                    "roster_bonus": val * 0.1
                })

            contracts.append({
                "player_id": p['gsis_id'],
                "team_abbr": p['team_abbr'],
                "total_value": val * length,
                "avg_annual": val,
                "contract_length": length,
                "year_signed": year_signed,
                "years": years_data
            })
        return contracts

    @staticmethod
    def generate_bulk_stats(players: List[Dict], season: int = 2023) -> List[Dict]:
        stats = []
        for p in players:
            epa = random.normalvariate(10, 30)
            if p['position'] == "QB": epa = random.normalvariate(150, 80)
            elif p['position'] in ["RB", "WR"]: epa = random.normalvariate(40, 20)
            
            stats.append({
                "player_id": p['gsis_id'],
                "season": season,
                "total_epa": round(epa, 1),
                "games": random.randint(1, 17),
                "fantasy_points_ppr": round(epa * 1.5 + random.uniform(0, 50), 1)
            })
        return stats

class OffseasonBattleSimulator:

    def __init__(self, league_cap: float = 255.4):
        self.league_cap = league_cap
        self.results = {}

    def run_league_simulation(self, players: List[Dict], contracts: List[Dict], stats: List[Dict]):
        from backend.app.services.optimizer import RosterOptimizer
        
        teams = set(p['team_abbr'] for p in players)
        
        for team in teams:
            team_players = [p for p in players if p['team_abbr'] == team]
            team_contracts = [c for c in contracts if c['team_abbr'] == team]
            
            total_cap = 0
            roster_data = []
            for tc in team_contracts:
                y2024 = next((y for y in tc['years'] if y['year'] == 2024), None)
                if y2024:
                    total_cap += y2024['cap_number']
                    p_stats = next((s for s in stats if s['player_id'] == tc['player_id']), {"total_epa": 0.0})
                    p_info = next((p for p in players if p['gsis_id'] == tc['player_id']))
                    
                    from backend.app.models.contract import Contract, ContractYear
                    c_obj = Contract(player_id=tc['player_id'])
                    c_obj.years = [ContractYear(**y) for y in tc['years']]

                    roster_data.append({
                        "name": p_info['name'],
                        "cap_hit": y2024['cap_number'],
                        "base_salary": y2024['base_salary'],
                        "total_epa": p_stats['total_epa'],
                        "contract_obj": c_obj
                    })

            over_by = total_cap - self.league_cap
            
            if over_by > 0:
                logger.info(f"Team {team} is OVER CAP by ${over_by:.2f}M. Running optimizer...")
                opt_res = RosterOptimizer.find_optimal_cap_fixes(roster_data, over_by)
                self.results[team] = {
                    "status": "Fixed" if opt_res['is_target_met'] else "Cap Hell",
                    "initial": total_cap,
                    "target_savings": over_by,
                    "achieved": opt_res['achieved_savings'],
                    "moves_count": len(opt_res['suggested_moves'])
                }
            else:
                self.results[team] = {"status": "Compliant", "initial": total_cap}

    def get_simulation_report(self) -> str:
        lines = ["🏁 LEAGUE-WIDE OFFSEASON BATTLE REPORT", "=" * 50]
        
        fixed = len([t for t in self.results.values() if t['status'] == "Fixed"])
        compliant = len([t for t in self.results.values() if t['status'] == "Compliant"])
        failed = len([t for t in self.results.values() if t['status'] == "Cap Hell"])
        
        lines.append(f"Total Teams Processed: {len(self.results)}")
        lines.append(f"Initially Compliant: {compliant}")
        lines.append(f"Optimized to Compliance: {fixed}")
        lines.append(f"Critical Failures (Cap Hell): {failed}")
        
        lines.append("\nDETAILED BREAKDOWN:")
        for team, res in self.results.items():
            lines.append(f" {team}: {res['status']} (Start: ${res['initial']:.1f}M)")
            
        return "\n".join(lines)
