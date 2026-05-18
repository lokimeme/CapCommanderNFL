import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("CapCommanderAudit")

class LeagueFinancialAudit:

    @staticmethod
    def calculate_parity_index(team_caps: List[Dict]) -> Dict:
        df = pd.DataFrame(team_caps)
        if df.empty: return {}
        
        std_dev = df['cap_space'].std()
        
        max_cap = df['cap_space'].max()
        min_cap = df['cap_space'].min()
        spread = max_cap - min_cap
        
        caps = sorted(df['cap_space'].values)
        n = len(caps)
        index = np.arange(1, n + 1)
        adj_caps = [c + abs(min_cap) + 1 for c in caps] 
        gini = ((np.sum((2 * index - n - 1) * adj_caps)) / (n * np.sum(adj_caps)))
        
        return {
            "standard_deviation": round(std_dev, 2),
            "spread_range": round(spread, 2),
            "gini_index": round(gini, 3),
            "parity_status": "High" if gini < 0.2 else "Moderate" if gini < 0.4 else "Low"
        }

    @staticmethod
    def audit_guaranteed_exposure(contracts: List[Dict]) -> Dict:
        df = pd.DataFrame(contracts)
        if df.empty: return {}
        
        total_guaranteed = df['total_guaranteed'].sum()
        avg_per_team = total_guaranteed / 32
        
        by_pos = df.groupby('position')['total_guaranteed'].sum().sort_values(ascending=False)
        
        return {
            "league_total_debt": round(total_guaranteed, 2),
            "avg_guarantee_per_team": round(avg_per_team, 2),
            "positional_concentration": by_pos.to_dict()
        }

    @staticmethod
    def identify_financial_red_flags(teams_data: List[Dict]) -> List[Dict]:
        flags = []
        for t in teams_data:
            reasons = []
            if t['dead_cap'] > 40.0:
                reasons.append(f"Excessive Dead Cap (${t['dead_cap']}M)")
            
            if t['future_obligations'] > 250.0:
                reasons.append(f"Dangerous Future Obligations (${t['future_obligations']}M)")
                
            if t['roster_health_score'] < 60.0:
                reasons.append(f"Low Roster Efficiency Score ({t['roster_health_score']})")
                
            if reasons:
                flags.append({
                    "team": t['team_abbr'],
                    "risk_level": "Critical" if len(reasons) >= 3 else "Moderate",
                    "red_flags": reasons
                })
                
        return sorted(flags, key=lambda x: len(x['red_flags']), reverse=True)

    @staticmethod
    def generate_league_audit_report(team_stats: List[Dict], leaguewide_debt: Dict) -> str:
        parity = LeagueFinancialAudit.calculate_parity_index(team_stats)
        flags = LeagueFinancialAudit.identify_financial_red_flags(team_stats)
        
        lines = ["🏢 LEAGUE-WIDE FINANCIAL AUDIT", "=" * 50]
        lines.append(f"League Parity Status: {parity['parity_status']} (Gini: {parity['gini_index']})")
        lines.append(f"Total Guaranteed Commitment: ${leaguewide_debt['league_total_debt']}M")
        
        lines.append("\nPOSITIONAL DEBT CONCENTRATION:")
        for pos, val in list(leaguewide_debt['positional_concentration'].items())[:5]:
            lines.append(f" - {pos}: ${val:.1f}M")
            
        lines.append("\nTEAMS IN FINANCIAL DISTRESS:")
        if not flags:
            lines.append(" - No teams currently flagged for high-risk profiles.")
        else:
            for f in flags:
                lines.append(f" 🚩 {f['team']} ({f['risk_level']}): {', '.join(f['red_flags'])}")
                
        return "\n".join(lines)
