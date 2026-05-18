import pandas as pd
import numpy as np

def calculate_cut_outcomes(contract_row, current_year=2024):
    """
    Calculates the financial impact of cutting a player.
    
    Args:
        contract_row: A row from the contracts DataFrame (with 'cols' struct)
        current_year: The year to analyze
        
    Returns:
        dict: Pre-June 1 and Post-June 1 outcomes
    """
    cols = contract_row.get('cols', [])
    if not cols:
        return None
    
    # Filter for future years including current
    future_years = [c for c in cols if c['year'].isdigit() and int(c['year']) >= current_year]
    if not future_years:
        return None
        
    current_year_data = next((c for c in future_years if int(c['year']) == current_year), None)
    if not current_year_data:
        return None

    cap_number = current_year_data.get('cap_number', 0)
    
    # Total remaining prorated bonus (including current year)
    total_remaining_prorated = sum(c.get('prorated_bonus', 0) or 0 for c in future_years)
    
    # Guaranteed salary for the current year (that hasn't been paid)
    # Note: In a real forensic tool, we'd check if salary is fully guaranteed.
    # For now, we use the 'guaranteed_salary' field from OTC data.
    guaranteed_current = current_year_data.get('guaranteed_salary', 0) or 0
    
    # --- Pre-June 1st Cut ---
    # All remaining prorated bonus hits NOW
    pre_june_dead_cap = total_remaining_prorated + guaranteed_current
    pre_june_savings = cap_number - pre_june_dead_cap
    
    # --- Post-June 1st Cut ---
    # Current year's prorated bonus + current guaranteed hits NOW
    # Remaining prorated bonus hits NEXT year
    current_prorated = current_year_data.get('prorated_bonus', 0) or 0
    post_june_dead_cap_current = current_prorated + guaranteed_current
    post_june_savings = cap_number - post_june_dead_cap_current
    
    # Future dead cap (hits next year)
    post_june_dead_cap_future = total_remaining_prorated - current_prorated
    
    return {
        'player': contract_row['player'],
        'cap_number': cap_number,
        'pre_june': {
            'dead_cap': pre_june_dead_cap,
            'savings': pre_june_savings
        },
        'post_june': {
            'dead_cap_current': post_june_dead_cap_current,
            'dead_cap_future': post_june_dead_cap_future,
            'savings': post_june_savings
        }
    }

def get_team_forensics(contracts_df, team_name, year=2024):
    team_contracts = contracts_df[contracts_df['team'] == team_name]
    results = []
    for _, row in team_contracts.iterrows():
        outcome = calculate_cut_outcomes(row, year)
        if outcome:
            results.append(outcome)
    return pd.DataFrame(results)
