import pytest
from backend.app.services.scouting_pro import ProspectScoutingEngine

def test_prospect_grade_generational():
    combine = {"ras": 9.8}
    tape = 9.5
    prod = {"dominator_rating": 0.45, "yards_per_route_run": 3.2}
    
    grade = ProspectScoutingEngine.calculate_prospect_grade(combine, tape, prod)
    
    assert grade['composite_grade'] >= 9.0
    assert grade['tier'] == "Generational Prospect"

def test_identify_sleepers():
    prospects = [
        {"name": "Fast Guy", "position": "WR", "game_tape_score": 5.0, "ras": 9.9}, # Workout warrior
        {"name": "Technical Guy", "position": "WR", "game_tape_score": 8.5, "ras": 3.5}, # Sleeper
    ]
    
    sleepers = ProspectScoutingEngine.identify_draft_sleepers(prospects)
    
    assert len(sleepers) == 1
    assert sleepers[0]['name'] == "Technical Guy"

def test_draft_board_generation():
    prospects = [
        {"name": "QB1", "position": "QB", "composite_grade": 9.0},
        {"name": "WR1", "position": "WR", "composite_grade": 8.5},
    ]
    needs = {"WR": {"priority": "Critical"}} # WR should jump QB
    
    board = ProspectScoutingEngine.generate_draft_board(prospects, needs)
    
    assert board[0]['name'] == "WR1" # Adjusted grade 8.5 * 1.25 = 10.6
    assert board[1]['name'] == "QB1"

def test_mock_draft_simulation():
    board = [
        {"name": "P1", "position": "QB"},
        {"name": "P2", "position": "WR"},
        {"name": "P3", "position": "OT"},
    ]
    team_slots = [2] # Team has the #2 overall pick
    
    selections = ProspectScoutingEngine.simulate_mock_draft(board, team_slots)
    
    assert len(selections) == 1
    assert selections[0]['player'] == "P2" # Slot 2 (index 1)
