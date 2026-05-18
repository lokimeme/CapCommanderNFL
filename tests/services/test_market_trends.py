import pytest
from backend.app.services.market_trends import MarketTrendAnalyzer

def test_positional_inflation():
    contracts = [
        {"position": "WR", "year_signed": 2020, "avg_annual": 15.0},
        {"position": "WR", "year_signed": 2020, "avg_annual": 14.0},
        {"position": "WR", "year_signed": 2023, "avg_annual": 30.0},
        {"position": "WR", "year_signed": 2023, "avg_annual": 28.0},
    ]
    years = [2020, 2023]
    
    report = MarketTrendAnalyzer.calculate_positional_inflation(contracts, years)
    
    assert "WR" in report
    assert report["WR"]["total_growth"] == 100.0 # (29.0 / 14.5) - 1
    assert report["WR"]["cagr"] > 0

def test_market_inefficiencies():
    # Mock skewed market
    contracts = [
        {"position": "QB", "avg_annual": 50.0},
        {"position": "QB", "avg_annual": 48.0},
        {"position": "QB", "avg_annual": 45.0},
        {"position": "QB", "avg_annual": 10.0},
        {"position": "QB", "avg_annual": 5.0},
        {"position": "QB", "avg_annual": 1.0},
        {"position": "QB", "avg_annual": 0.8},
        {"position": "QB", "avg_annual": 0.8},
        {"position": "QB", "avg_annual": 0.8},
        {"position": "QB", "avg_annual": 0.8},
    ]
    
    report = MarketTrendAnalyzer.detect_market_inefficiencies(contracts)
    
    assert len(report) > 0
    assert report[0]['position'] == "QB"
    assert report[0]['verdict'] == "Top-Heavy (Stars & Scrubs)"

def test_cap_limit_prediction():
    hist_caps = {
        2020: 198.2,
        2021: 182.5, # Covid drop
        2022: 208.2,
        2023: 224.8,
        2024: 255.4
    }
    
    prediction = MarketTrendAnalyzer.predict_future_cap_limit(hist_caps, 2025)
    
    assert prediction > 255.4
    assert isinstance(prediction, float)
