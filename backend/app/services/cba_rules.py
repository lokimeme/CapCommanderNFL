from typing import Dict, List, Optional
from backend.app.models.contract import Contract, ContractYear
import math

def calculate_detailed_cut_impact(contract: Contract, current_year: int) -> Dict:
    years = sorted(contract.years, key=lambda x: x.year)
    future_years = [y for y in years if y.year >= current_year]
    
    if not future_years:
        return {}

    current_year_data = next((y for y in future_years if y.year == current_year), None)
    if not current_year_data:
        return {}

    cap_hit = current_year_data.cap_number
    
    total_remaining_signing = sum(y.signing_bonus or 0 for y in future_years)
    
    pre_june_dead_cap = total_remaining_signing
    pre_june_savings = cap_hit - pre_june_dead_cap
    
    post_june_dead_cap_current = current_year_data.signing_bonus or 0
    post_june_savings = cap_hit - post_june_dead_cap_current
    
    post_june_dead_cap_future = total_remaining_signing - post_june_dead_cap_current
    
    return {
        "player_id": contract.player_id,
        "current_cap_hit": cap_hit,
        "pre_june_1": {
            "dead_cap": pre_june_dead_cap,
            "savings": pre_june_savings
        },
        "post_june_1": {
            "dead_cap_current": post_june_dead_cap_current,
            "dead_cap_future": post_june_dead_cap_future,
            "savings": post_june_savings
        }
    }

def estimate_franchise_tag(position: str, year: int) -> float:
    tags = {
        "QB": 38.3,
        "RB": 11.9,
        "WR": 21.8,
        "TE": 12.7,
        "OL": 20.9,
        "DE": 21.3,
        "DT": 22.1,
        "LB": 24.0,
        "CB": 19.8,
        "S": 17.1,
        "K/P": 5.9
    }
    return tags.get(position, 15.0)

def calculate_fifth_year_option(player: "Player", performance_tier: str = "Basic") -> Optional[float]:
    if player.draft_round != 1:
        return None
    
    base_values = {
        "QB": 20.0, "RB": 10.0, "WR": 15.0, "TE": 10.0, "OL": 14.0, 
        "DE": 17.0, "DT": 16.0, "LB": 18.0, "CB": 13.0, "S": 12.0
    }
    
    multiplier = 1.0
    if performance_tier == "Playtime": multiplier = 1.1
    elif performance_tier == "1 Pro Bowl": multiplier = 1.3
    elif performance_tier == "2+ Pro Bowls": multiplier = 1.5
    
    base = base_values.get(player.position, 12.0)
    return round(base * multiplier, 2)

def calculate_compensatory_pick_estimate(lost_players: List[Dict], gained_players: List[Dict]) -> Dict:
    salary_threshold = 2.5
    
    q_lost = [p for p in lost_players if p['avg_annual_salary'] >= salary_threshold]
    q_gained = [p for p in gained_players if p['avg_annual_salary'] >= salary_threshold]
    
    net_diff = len(q_lost) - len(q_gained)
    
    if net_diff <= 0:
        return {"total_picks": 0, "details": "No net loss of qualifying free agents."}
        
    picks = []
    q_lost_sorted = sorted(q_lost, key=lambda x: x['avg_annual_salary'], reverse=True)
    
    for i in range(net_diff):
        player = q_lost_sorted[i]
        salary = player['avg_annual_salary']
        
        if salary >= 20.0: round_val = 3
        elif salary >= 15.0: round_val = 4
        elif salary >= 10.0: round_val = 5
        elif salary >= 5.0: round_val = 6
        else: round_val = 7
        
        picks.append({
            "player": player['name'],
            "projected_round": round_val,
            "value_metric": salary
        })
        
    return {
        "total_picks": len(picks),
        "picks": picks,
        "formula_summary": f"Net loss of {net_diff} qualifying free agents."
    }
