import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activity_state():
    original_state = {
        name: copy.deepcopy(details)
        for name, details in app_module.activities.items()
    }
    yield
    app_module.activities.clear()
    app_module.activities.update(original_state)


def test_signup_and_unregister_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert signup_response.status_code == 200
    signup_payload = signup_response.json()
    assert email in signup_payload["activities"][activity_name]["participants"]
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
