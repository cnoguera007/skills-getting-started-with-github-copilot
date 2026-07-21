from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_from_activity():
    original_participants = activities["Chess Club"]["participants"][:]

    try:
        response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

        assert response.status_code == 200
        data = response.json()
        assert "michael@mergington.edu" not in data["participants"]
        assert "daniel@mergington.edu" in data["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants
