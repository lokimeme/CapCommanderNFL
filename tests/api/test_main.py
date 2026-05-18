from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CapCommander NFL Enterprise API"}

def test_read_teams():
    response = client.get("/teams/")
    # If no data ingested yet, it should return an empty list or be 200
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_players_filtered():
    response = client.get("/players/", params={"team_abbr": "KC"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_player_not_found():
    response = client.get("/players/NON_EXISTENT_ID")
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"
