from typing import List, Dict, Optional
from backend.app.services.cba_rules import calculate_detailed_cut_impact
from backend.app.services.trade_engine import calculate_player_trade_impact
from backend.app.services.draft_modeling import estimate_rookie_cap_hit
import logging

logger = logging.getLogger("CapCommanderSimulator")

class ScenarioSession:
    def __init__(self, team_abbr: str, starting_cap_space: float, year: int = 2024):
        self.team_abbr, self.year = team_abbr, year
        self.starting_cap_space = self.current_cap_space = starting_cap_space
        self.transactions, self.dead_cap_total = [], 0
        self.future_year_obligations = {y: 0.0 for y in range(year + 1, year + 5)}
        self.roster_count = 53

    def execute_cut(self, player_name: str, contract: Dict, is_post_june: bool = False):
        impact = calculate_detailed_cut_impact(contract, self.year)
        if not impact: return
        move_type = "post_june_1" if is_post_june else "pre_june_1"
        savings = impact[move_type]["savings"]
        dead_cap = impact[move_type]["dead_cap"] if not is_post_june else impact[move_type]["dead_cap_current"]
        self.current_cap_space += savings
        self.dead_cap_total += dead_cap
        self.roster_count -= 1
        if is_post_june: self.future_year_obligations[self.year + 1] += impact[move_type]["dead_cap_future"]
        self.transactions.append({
            "type": f"CUT ({move_type})", "player": player_name,
            "savings": round(savings, 2), "dead_cap_added": round(dead_cap, 2), "roster_delta": -1
        })

    def execute_trade(self, player_name: str, contract: Dict, retention: float = 0.0):
        impact = calculate_player_trade_impact(contract, self.year, retention)
        if not impact: return
        savings, dead_cap = impact["trading_team"]["immediate_savings"], impact["trading_team"]["dead_cap_added"]
        self.current_cap_space += savings
        self.dead_cap_total += dead_cap
        self.roster_count -= 1
        self.transactions.append({
            "type": f"TRADE (Retention: {retention*100}%)", "player": player_name,
            "savings": round(savings, 2), "dead_cap_added": round(dead_cap, 2), "roster_delta": -1
        })

    def sign_free_agent(self, player_name: str, annual_salary: float, contract_length: int, signing_bonus: float = 0.0):
        annual_proration = signing_bonus / contract_length
        year_1_cap_hit = (annual_salary - (signing_bonus/contract_length)) + annual_proration
        self.current_cap_space -= year_1_cap_hit
        self.roster_count += 1
        for y in range(self.year + 1, self.year + contract_length):
            if y in self.future_year_obligations: self.future_year_obligations[y] += annual_salary
        self.transactions.append({
            "type": "FREE AGENT SIGNING", "player": player_name,
            "savings": -round(year_1_cap_hit, 2), "details": f"{contract_length}y, ${annual_salary}M APY"
        })

    def model_draft_class(self, picks: List[int]):
        pool_cost = sum(estimate_rookie_cap_hit(p, self.year)["year_1_cap_hit"] for p in picks)
        self.current_cap_space -= pool_cost
        self.roster_count += len(picks)
        self.transactions.append({
            "type": "ROOKIE POOL", "player": f"{len(picks)} Picks",
            "savings": -round(pool_cost, 2), "details": f"Projected pool."
        })

    def run_compliance_check(self) -> Dict:
        warnings = []
        if self.current_cap_space < 0: warnings.append("⚠️ OVER CAP")
        if self.roster_count < 53: warnings.append(f"ℹ️ UNDER-STRENGTH: {self.roster_count}/53")
        p_caps = {2025: 260.0, 2026: 285.0, 2027: 310.0}
        for y, obligation in self.future_year_obligations.items():
            if y in p_caps and obligation > p_caps[y] * 0.8: warnings.append(f"🚩 CAP HELL ALERT: {y}")
        return {
            "is_compliant": self.current_cap_space >= 0 and self.roster_count >= 53,
            "warnings": warnings, "roster_count": self.roster_count,
            "net_savings": round(self.current_cap_space - self.starting_cap_space, 2)
        }

    def get_summary_report(self) -> str:
        lines = [f"📊 OFFSEASON SUMMARY: {self.team_abbr} ({self.year})", "=" * 40]
        lines.append(f"Start: ${self.starting_cap_space}M | End: ${round(self.current_cap_space, 2)}M")
        lines.append(f"Net: ${round(self.current_cap_space - self.starting_cap_space, 2)}M | Dead: ${round(self.dead_cap_total, 2)}M")
        lines.append(f"Roster: {self.roster_count}/53")
        lines.append("\nTRANSACTION LEDGER:")
        for t in self.transactions:
            s = "✅" if t['savings'] >= 0 else "💸"
            lines.append(f" {s} {t['type']}: {t['player']} ({t['savings']}M)")
        return "\n".join(lines)
