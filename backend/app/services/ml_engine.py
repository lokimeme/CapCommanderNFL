import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Dict
from backend.app.models.player import Player
from backend.app.models.stats import SeasonalStats

def calculate_mvd_albatross(players_stats: List[Dict]) -> pd.DataFrame:
    POSITION_MULTIPLIERS = {
        "QB": 1.5, "LT": 1.3, "OT": 1.25, "EDGE": 1.3, "DE": 1.2,
        "WR": 1.2, "CB": 1.2, "K": 0.8, "P": 0.7, "LS": 0.5
    }
    df = pd.DataFrame(players_stats)
    if df.empty: return df
    df['weighted_epa'] = df.apply(
        lambda row: row['total_epa'] * POSITION_MULTIPLIERS.get(row['position'], 1.0),
        axis=1
    )
    results = []
    for pos in df['position'].unique():
        pos_df = df[df['position'] == pos].copy()
        if len(pos_df) < 5: 
            pos_df['expected_cap_hit'] = pos_df['cap_hit']
            pos_df['mvd'] = 0
            results.append(pos_df)
            continue
        X = pos_df[['weighted_epa']].values
        y = pos_df['cap_hit'].values
        model = LinearRegression()
        model.fit(X, y)
        pos_df['expected_cap_hit'] = model.predict(X)
        pos_df['mvd'] = pos_df['cap_hit'] - pos_df['expected_cap_hit']
        results.append(pos_df)
    return pd.concat(results)

def predict_performance_decline(player_age: int, position: str, current_epa: float) -> float:
    aging_curves = {
        "QB": { "peak": 29, "decline_rate": 0.05 },
        "RB": { "peak": 25, "decline_rate": 0.15 },
        "WR": { "peak": 27, "decline_rate": 0.08 },
        "CB": { "peak": 26, "decline_rate": 0.10 },
        "OL": { "peak": 30, "decline_rate": 0.04 }
    }
    curve = aging_curves.get(position, {"peak": 27, "decline_rate": 0.10})
    if player_age <= curve["peak"]:
        return current_epa * 1.02
    else:
        years_past_peak = player_age - curve["peak"]
        decline = 1 - (curve["decline_rate"] * years_past_peak)
        return current_epa * max(decline, 0.1)
