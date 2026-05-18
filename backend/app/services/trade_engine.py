from typing import List, Dict, Optional, Tuple
from backend.app.models.contract import Contract, ContractYear
from backend.app.services.team_needs import TeamNeedsService
from backend.app.services.draft_modeling import DraftValueCharts
import logging

logger = logging.getLogger("CapCommanderTrade")

class TradeAsset:
    def __init__(self, asset_type: str, details: Dict):
        self.asset_type = asset_type
        self.details = details

class TradeOutcome:
    def __init__(self):
        self.team_summaries = {}

def simulate_multi_team_trade(trade_config: List[Dict], current_year: int = 2024) -> Dict:
    outcomes = {}
    def init_team(team):
        if team not in outcomes:
            outcomes[team] = {
                "cap_savings": 0.0, "cap_absorbed": 0.0, "dead_cap_added": 0.0,
                "picks_lost": [], "picks_gained": [], "net_value_delta": 0.0
            }

    for move in trade_config:
        from_team = move["from_team"]
        to_team = move["to_team"]
        asset = move["asset"]
        init_team(from_team)
        init_team(to_team)
        if asset["type"] == "player":
            contract = asset["contract"]
            retention = asset.get("retention_pct", 0.0)
            impact = calculate_player_trade_impact(contract, current_year, retention)
            outcomes[from_team]["cap_savings"] += impact["trading_team"]["immediate_savings"]
            outcomes[from_team]["dead_cap_added"] += impact["trading_team"]["dead_cap_added"]
            outcomes[to_team]["cap_absorbed"] += impact["receiving_team"]["new_cap_hit"]
        elif asset["type"] == "pick":
            pick_num = asset["pick_number"]
            value = DraftValueCharts.get_jimmy_johnson_value(pick_num)
            outcomes[from_team]["picks_lost"].append(pick_num)
            outcomes[to_team]["picks_gained"].append(pick_num)
            outcomes[from_team]["net_value_delta"] -= value
            outcomes[to_team]["net_value_delta"] += value

    for team, stats in outcomes.items():
        stats["net_cap_impact"] = stats["cap_savings"] - stats["cap_absorbed"]
    return outcomes

def calculate_player_trade_impact(contract: Contract, current_year: int, retention_pct: float = 0.0) -> Dict:
    years = sorted(contract.years, key=lambda x: x.year)
    current_year_data = next((y for y in years if y.year == current_year), None)
    if not current_year_data:
        return {"trading_team": {"dead_cap_added": 0, "immediate_savings": 0}, "receiving_team": {"new_cap_hit": 0}}
    future_years = [y for y in years if y.year >= current_year]
    total_remaining_prorated = sum(y.signing_bonus or 0 for y in future_years)
    trading_team_dead_cap = total_remaining_prorated
    current_cap_hit = current_year_data.cap_number
    prorated_bonus_current = current_year_data.signing_bonus or 0
    base_savings = current_cap_hit - prorated_bonus_current
    retained_amount = 0.0
    if retention_pct > 0:
        base_salary = current_year_data.base_salary or 0
        retained_amount = base_salary * retention_pct
    trading_team_dead_cap += retained_amount
    final_trading_savings = base_savings - retained_amount
    receiving_team_cap_hit = (current_year_data.base_salary or 0) + \
                             (current_year_data.roster_bonus or 0) + \
                             (current_year_data.option_bonus or 0) - retained_amount
    return {
        "trading_team": {
            "dead_cap_added": round(trading_team_dead_cap, 2),
            "immediate_savings": round(final_trading_savings, 2),
            "retention_paid": round(retained_amount, 2)
        },
        "receiving_team": { "new_cap_hit": round(receiving_team_cap_hit, 2) }
    }

def evaluate_trade_success_probability(from_team_needs: Dict, to_team_needs: Dict, player_data: Dict) -> float:
    fit_analysis = TeamNeedsService.evaluate_trade_strategic_fit("placeholder", to_team_needs, player_data)
    return fit_analysis["strategic_score"] / 100.0

def generate_multi_team_trade_report(results: Dict) -> str:
    lines = ["🏈 MULTI-TEAM TRADE ADVISORY REPORT", "=" * 40]
    for team, stats in results.items():
        lines.append(f"\nTEAM: {team}")
        lines.append(f"  - Cap Delta: {'+' if stats['net_cap_impact'] >= 0 else ''}{stats['net_cap_impact']:.2f}M")
        lines.append(f"  - Dead Cap Acceleration: {stats['dead_cap_added']:.2f}M")
        if stats["picks_gained"]: lines.append(f"  - Picks Acquired: {', '.join(map(str, stats['picks_gained']))}")
        if stats["picks_lost"]: lines.append(f"  - Picks Relinquished: {', '.join(map(str, stats['picks_lost']))}")
    return "\n".join(lines)
