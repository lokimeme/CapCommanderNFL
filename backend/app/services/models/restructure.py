import pandas as pd
import numpy as np

def simulate_simple_restructure(cap_hit, base_salary, dead_cap, years_remaining, min_salary=0.75):
    """
    Simulates a standard restructure: converting base salary to signing bonus.
    
    Args:
        cap_hit: Current year cap hit
        base_salary: Current year base salary
        dead_cap: Current year dead cap
        years_remaining: Remaining years on contract (including current)
        min_salary: The league minimum salary that must remain as base
        
    Returns:
        dict: New cap hit, savings, and remaining dead cap spread
    """
    if base_salary <= min_salary:
        return {
            'new_cap_hit': cap_hit,
            'savings': 0,
            'restructure_amount': 0,
            'proration_increase': 0
        }
    
    # Amount to convert
    convertible_amount = base_salary - min_salary
    
    # Prorate over remaining years (max 5 years usually, but we'll use years_remaining for simplicity)
    # Most restructures spread over the length of the deal
    proration_years = min(years_remaining, 5)
    annual_proration = convertible_amount / proration_years
    
    new_cap_hit = cap_hit - convertible_amount + annual_proration
    savings = cap_hit - new_cap_hit
    
    return {
        'new_cap_hit': new_cap_hit,
        'savings': savings,
        'restructure_amount': convertible_amount,
        'annual_proration_increase': annual_proration,
        'proration_years': proration_years
    }

def simulate_void_year_restructure(cap_hit, base_salary, years_remaining, void_years=1, min_salary=0.75):
    """
    Simulates a restructure with added void years for maximum proration.
    """
    convertible_amount = base_salary - min_salary
    
    # Prorate over remaining years + void years (cap at 5 years total)
    total_years = years_remaining + void_years
    proration_years = min(total_years, 5)
    
    annual_proration = convertible_amount / proration_years
    
    new_cap_hit = cap_hit - convertible_amount + annual_proration
    savings = cap_hit - new_cap_hit
    
    return {
        'new_cap_hit': new_cap_hit,
        'savings': savings,
        'restructure_amount': convertible_amount,
        'annual_proration_increase': annual_proration,
        'proration_years': proration_years,
        'void_years_added': void_years
    }
