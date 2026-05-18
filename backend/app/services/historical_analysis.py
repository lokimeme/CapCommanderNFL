from typing import List, Dict

class HistoricalCapBenchmarks:
    
    BENCHMARKS = {
        "QB": {"avg_pct": 12.5, "range": [0.5, 17.5], "note": "Brady/Mahomes outliers vs rookie contracts"},
        "OL": {"avg_pct": 18.2, "range": [14.0, 22.0], "note": "High investment in protection is common"},
        "DL": {"avg_pct": 16.5, "range": [12.0, 21.0], "note": "The foundation of modern NFL defenses"},
        "WR": {"avg_pct": 9.8, "range": [5.0, 15.0], "note": "Often lower for champions unless elite talent"},
        "DB": {"avg_pct": 14.2, "range": [10.0, 18.0], "note": "Critical for passing league defense"},
        "LB": {"avg_pct": 7.5, "range": [4.0, 11.0], "note": "Declining value in sub-package eras"},
        "ST": {"avg_pct": 2.5, "range": [1.5, 4.0], "note": "Consistent small investment"},
        "RB": {"avg_pct": 3.8, "range": [1.0, 7.0], "note": "Lowest investment among starters"}
    }

    @classmethod
    def get_positional_benchmark(cls, position: str) -> Dict:
        mapping = {
            "OT": "OL", "OG": "OL", "C": "OL",
            "DE": "DL", "DT": "DL", "EDGE": "DL",
            "CB": "DB", "S": "DB", "FS": "DB", "SS": "DB",
            "ILB": "LB", "OLB": "LB",
            "K": "ST", "P": "ST", "LS": "ST"
        }
        
        group = mapping.get(position, position)
        return cls.BENCHMARKS.get(group, {"avg_pct": 0, "range": [0, 0], "note": "No benchmark available"})

    @classmethod
    def analyze_roster_allocation(cls, roster_cap_hits: List[Dict]) -> Dict:
        total_cap = sum(p['cap_hit'] for p in roster_cap_hits)
        if total_cap == 0: return {}
        
        allocation = {}
        for p in roster_cap_hits:
            pos = p['position']
            mapping = {
                "OT": "OL", "OG": "OL", "C": "OL",
                "DE": "DL", "DT": "DL", "EDGE": "DL",
                "CB": "DB", "S": "DB", "FS": "DB", "SS": "DB",
                "ILB": "LB", "OLB": "LB"
            }
            group = mapping.get(pos, pos)
            allocation[group] = allocation.get(group, 0) + p['cap_hit']
            
        results = {}
        for group, amount in allocation.items():
            pct = (amount / total_cap) * 100
            benchmark = cls.get_positional_benchmark(group)
            
            status = "Optimal"
            if pct > benchmark['range'][1]: status = "Over-Invested"
            elif pct < benchmark['range'][0]: status = "Under-Invested"
            
            results[group] = {
                "current_pct": round(pct, 1),
                "benchmark_avg": benchmark['avg_pct'],
                "status": status,
                "note": benchmark['note']
            }
            
        return results
