from typing import List, Dict, Optional

class DraftValueCharts:
    
    @staticmethod
    def get_jimmy_johnson_value(pick_number: int) -> float:
        if pick_number == 1: return 3000
        if pick_number == 2: return 2600
        if pick_number == 3: return 2200
        if pick_number == 10: return 1300
        if pick_number == 32: return 590
        
        return round(3000 * (pick_number ** -0.6), 1)

    @staticmethod
    def get_chase_stuart_value(pick_number: int) -> float:
        if pick_number == 1: return 34.6
        if pick_number == 32: return 11.2
        return round(34.6 * (pick_number ** -0.35), 1)

def calculate_pick_swap_equity(gave_picks: List[int], received_picks: List[int], chart_type: str = "JJ") -> Dict:
    chart_func = DraftValueCharts.get_jimmy_johnson_value if chart_type == "JJ" else DraftValueCharts.get_chase_stuart_value
    
    gave_total = sum(chart_func(p) for p in gave_picks)
    received_total = sum(chart_func(p) for p in received_picks)
    
    delta = received_total - gave_total
    equity_pct = (received_total / gave_total) if gave_total > 0 else 0
    
    return {
        "gave_value": gave_total,
        "received_value": received_total,
        "delta": delta,
        "equity_pct": round(equity_pct * 100, 1),
        "verdict": "Fair" if 0.9 <= equity_pct <= 1.1 else "Lopsided"
    }

def estimate_rookie_cap_hit(pick_number: int, current_year: int) -> Dict:
    if pick_number == 1: 
        total_value = 39.4
        signing_bonus = 24.5
    elif pick_number == 32:
        total_value = 12.1
        signing_bonus = 5.6
    else:
        total_value = 40.0 * (pick_number ** -0.35)
        signing_bonus = total_value * 0.4
        
    avg_annual = total_value / 4
    year_1_cap = (signing_bonus / 4) + 0.795
    
    return {
        "pick": pick_number,
        "total_value": round(total_value, 2),
        "signing_bonus": round(signing_bonus, 2),
        "year_1_cap_hit": round(year_1_cap, 2),
        "is_fifth_year_eligible": pick_number <= 32
    }
