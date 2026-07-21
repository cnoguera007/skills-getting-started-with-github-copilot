import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = {}
    for activity_name, activity in activities.items():
        original[activity_name] = activity["participants"][:]
    yield
    for activity_name, participants in original.items():
        activities[activity_name]["participants"] = participants


def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_adds_participant(client):
    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert "student@mergington.edu" in data["participants"]


def test_unregister_participant_from_activity(client):
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert "michael@mergington.edu" not in data["participants"]


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
