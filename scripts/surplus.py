import pandas as pd
import numpy as np

def calculate_surplus_yield(contracts_df, seasonal_df, rosters_df, year=2023):
    """
    Calculates production-to-cost ratio.
    
    Args:
        contracts_df: DataFrame with contract info
        seasonal_df: DataFrame with performance data
        rosters_df: DataFrame with player IDs and team info
        year: The year to analyze
        
    Returns:
        pd.DataFrame: Players ranked by surplus value
    """
    # 1. Merge seasonal data with rosters to get team and name
    perf = seasonal_df[seasonal_df['season'] == year].copy()
    
    # 2. Join performance with contracts on gsis_id
    # contracts has 'gsis_id', seasonal has 'player_id'
    merged = pd.merge(
        perf, 
        contracts_df, 
        left_on='player_id', 
        right_on='gsis_id', 
        how='inner'
    )
    
    # 3. Get the cap hit for the specific year from 'cols'
    def get_cap_hit(cols, target_year):
        if not isinstance(cols, list): return np.nan
        for c in cols:
            if c['year'] == str(target_year):
                return c.get('cap_number', np.nan)
        return np.nan

    merged['year_cap_hit'] = merged['cols'].apply(lambda x: get_cap_hit(x, year))
    
    # Drop rows with no cap hit info
    merged = merged.dropna(subset=['year_cap_hit'])
    merged = merged[merged['year_cap_hit'] > 0]
    
    # 4. Calculate Surplus Metrics
    # Handle NaN values for EPA columns
    epa_cols = ['passing_epa', 'rushing_epa', 'receiving_epa']
    for col in epa_cols:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)
        else:
            merged[col] = 0
            
    merged['total_epa'] = merged['passing_epa'] + merged['rushing_epa'] + merged['receiving_epa']
    
    # Points per Million Dollars
    merged['points_per_million'] = merged['fantasy_points_ppr'] / merged['year_cap_hit']
    
    # EPA per Million Dollars
    merged['epa_per_million'] = merged['total_epa'] / merged['year_cap_hit']
    
    # Advanced metric: Value over Minimum (VOM)
    # Assuming a minimum cap hit of ~0.75M
    min_cap = 0.75
    merged['surplus_value'] = merged['fantasy_points_ppr'] * (1 - (merged['year_cap_hit'] / 50)) # Weighted by cost
    
    # Sort by EPA efficiency
    return merged.sort_values(by='epa_per_million', ascending=False)

def get_team_surplus(contracts_df, seasonal_df, team_nick, year=2023):
    all_surplus = calculate_surplus_yield(contracts_df, seasonal_df, None, year)
    return all_surplus[all_surplus['team'].str.contains(team_nick, na=False)]
