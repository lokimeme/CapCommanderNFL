import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from backend.app.models.contract import Contract, ContractYear
from backend.app.services.cba_rules import calculate_detailed_cut_impact
from backend.app.services.ml_engine import predict_performance_decline
import logging

logger = logging.getLogger("CapCommanderForensicPro")

class ForensicScoutingService:

    @staticmethod
    def generate_player_forensic_report(player: Dict, contract: Contract, current_year: int = 2024) -> Dict:
        years = sorted(contract.years, key=lambda x: x.year)
        
        exit_windows = []
        for y in years:
            if y.year < current_year: continue
            
            impact = calculate_detailed_cut_impact(contract, y.year)
            if not impact: continue
            
            savings = impact['pre_june_1']['savings']
            dead_cap = impact['pre_june_1']['dead_cap']
            
            eff_score = savings / (dead_cap + 0.1)
            
            status = "Negative"
            if savings > 5.0 and eff_score > 1.0: status = "Optimal"
            elif savings > 0: status = "Positive"
            
            exit_windows.append({
                "year": y.year,
                "savings": round(savings, 2),
                "dead_cap": round(dead_cap, 2),
                "efficiency": round(eff_score, 2),
                "verdict": status
            })

        current_epa = player.get('total_epa', 10.0)
        age = player.get('age', 26)
        pos = player.get('position', 'WR')
        
        cliffs = []
        projected_epa = current_epa
        for y in years:
            if y.year < current_year: continue
            
            projected_epa = predict_performance_decline(age + (y.year - current_year), pos, projected_epa)
            cap_hit = y.cap_number
            
            cost_per_epa = cap_hit / (projected_epa + 0.1)
            
            is_cliff = cost_per_epa > 2.0
            
            cliffs.append({
                "year": y.year,
                "projected_epa": round(projected_epa, 2),
                "cap_hit": round(cap_hit, 2),
                "cost_per_epa": round(cost_per_epa, 3),
                "is_danger_zone": is_cliff
            })

        total_guaranteed = contract.total_guaranteed or 0.0
        already_paid = sum(y.base_salary for y in years if y.year < current_year)
        remaining_guarantee = max(0, total_guaranteed - already_paid)
        
        guarantee_pct = (remaining_guarantee / (contract.total_value or 1.0)) * 100

        return {
            "player_name": player['name'],
            "position": pos,
            "exit_windows": exit_windows,
            "performance_projections": cliffs,
            "financial_summary": {
                "remaining_guarantee": round(remaining_guarantee, 2),
                "guarantee_exposure_pct": round(guarantee_pct, 1),
                "contract_status": "Secure" if guarantee_pct > 40 else "Flexible"
            }
        }

    @staticmethod
    def identify_optimal_exit_year(report: Dict) -> Optional[int]:
        windows = report.get('exit_windows', [])
        if not windows: return None
        
        best = max(windows, key=lambda x: x['efficiency'])
        return best['year']

    @staticmethod
    def format_forensic_advisory(report: Dict) -> str:
        lines = [f"🔍 FINANCIAL FORENSIC REPORT: {report['player_name']} ({report['position']})", "=" * 50]
        
        summary = report['financial_summary']
        lines.append(f"Contract Status: {summary['contract_status']}")
        lines.append(f"Remaining Guaranteed Exposure: ${summary['remaining_guarantee']}M ({summary['guarantee_exposure_pct']}%)")
        
        lines.append("\nSTRATEGIC EXIT WINDOWS:")
        for w in report['exit_windows']:
            status_emoji = "✅" if w['verdict'] == "Optimal" else "⚠️" if w['verdict'] == "Positive" else "❌"
            lines.append(f" {w['year']}: {status_emoji} Savings: ${w['savings']}M | Efficiency: {w['efficiency']}")

        lines.append("\nPRODUCTION-TO-COST CLIFFS:")
        for c in report['performance_projections']:
            danger = "🚩 [DANGER]" if c['is_danger_zone'] else "🟢 [VALUABLE]"
            lines.append(f" {c['year']}: {danger} | Est. EPA: {c['projected_epa']} | Cost/EPA: ${c['cost_per_epa']}M")
            
        return "\n".join(lines)
