import pandas as pd
import numpy as np

def get_multi_year_projections(team_contracts_df, start_year=2024, end_year=2026):
    """
    Aggregates cap hits across multiple years for a team.
    
    Args:
        team_contracts_df: DataFrame with contract info for a single team
        start_year: First year of projection
        end_year: Last year of projection
        
    Returns:
        pd.DataFrame: Projected total cap spending by year
    """
    years = list(range(start_year, end_year + 1))
    projections = []
    
    for year in years:
        year_total = 0
        for _, row in team_contracts_df.iterrows():
            contract_years = row['cols']
            if not isinstance(contract_years, list):
                continue
            
            year_data = next((c for c in contract_years if c['year'] == str(year)), None)
            if year_data:
                year_total += year_data.get('cap_number', 0)
        
        projections.append({
            'Year': year,
            'Total Projected Cap ($M)': round(year_total, 2)
        })
    
    return pd.DataFrame(projections)

def get_positional_breakdown(team_contracts_df, year=2024):
    """
    Calculates cap spending by position for a given year.
    """
    breakdown = []
    for _, row in team_contracts_df.iterrows():
        contract_years = row['cols']
        if not isinstance(contract_years, list):
            continue
        
        year_data = next((c for c in contract_years if c['year'] == str(year)), None)
        if year_data:
            breakdown.append({
                'Player': row['player'],
                'Position': row['position'],
                'Cap Hit': year_data.get('cap_number', 0)
            })
    
    df = pd.DataFrame(breakdown)
    if df.empty:
        return df
        
    return df.groupby('Position')['Cap Hit'].sum().reset_index().sort_values(by='Cap Hit', ascending=False)
