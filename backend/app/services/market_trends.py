import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("CapCommanderMarket")

class MarketTrendAnalyzer:

    @staticmethod
    def calculate_positional_inflation(historical_contracts: List[Dict], years: List[int]) -> Dict:
        df = pd.DataFrame(historical_contracts)
        if df.empty:
            return {}

        inflation_report = {}
        for pos in df['position'].unique():
            pos_data = df[df['position'] == pos]
            
            yearly_top_avg = []
            for year in sorted(years):
                year_data = pos_data[pos_data['year_signed'] == year]
                if year_data.empty: continue
                
                top_5_avg = year_data.sort_values(by='avg_annual', ascending=False).head(5)['avg_annual'].mean()
                yearly_top_avg.append({"year": year, "avg": top_5_avg})

            if len(yearly_top_avg) < 2: continue
            
            start = yearly_top_avg[0]['avg']
            end = yearly_top_avg[-1]['avg']
            n_years = len(yearly_top_avg) - 1
            
            if start > 0 and n_years > 0:
                cagr = (end / start) ** (1 / n_years) - 1
                inflation_report[pos] = {
                    "cagr": round(cagr * 100, 2),
                    "start_avg": round(start, 2),
                    "end_avg": round(end, 2),
                    "total_growth": round((end/start - 1) * 100, 2)
                }

        return inflation_report

    @staticmethod
    def detect_market_inefficiencies(all_contracts: List[Dict]) -> List[Dict]:
        df = pd.DataFrame(all_contracts)
        if df.empty:
            return []

        inefficiencies = []
        for pos in df['position'].unique():
            pos_df = df[df['position'] == pos]
            if len(pos_df) < 10: continue
            
            salaries = sorted(pos_df['avg_annual'].values)
            n = len(salaries)
            index = np.arange(1, n + 1)
            gini = ((np.sum((2 * index - n - 1) * salaries)) / (n * np.sum(salaries)))
            
            p40 = np.percentile(salaries, 40)
            p70 = np.percentile(salaries, 70)
            middle_count = len([s for s in salaries if p40 <= s <= p70])
            middle_density = middle_count / n
            
            verdict = "Balanced"
            if gini > 0.5: verdict = "Top-Heavy (Stars & Scrubs)"
            elif middle_density < 0.2: verdict = "Middle-Class Vacuum"
            elif gini < 0.2: verdict = "Flat Market (Commoditized)"

            inefficiencies.append({
                "position": pos,
                "gini_coefficient": round(gini, 3),
                "middle_density": round(middle_density, 2),
                "verdict": verdict,
                "avg_salary": round(pos_df['avg_annual'].mean(), 2)
            })

        return sorted(inefficiencies, key=lambda x: x['gini_coefficient'], reverse=True)

    @staticmethod
    def predict_future_cap_limit(historical_caps: Dict, target_year: int) -> float:
        years = sorted(historical_caps.keys())
        values = [historical_caps[y] for y in years]
        
        if len(years) < 3: return values[-1] * 1.08
        
        x = np.array(years)
        y = np.array(values)
        
        m, b = np.polyfit(x, y, 1)
        
        prediction = m * target_year + b
        return round(prediction, 1)
