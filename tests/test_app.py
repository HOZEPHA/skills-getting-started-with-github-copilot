import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activity_state():
    original_state = {
        name: copy.deepcopy(details)
        for name, details in app_module.activities.items()
    }
    yield
    app_module.activities.clear()
    app_module.activities.update(original_state)


client = TestClient(app_module.app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "student@example.com"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    payload = signup_response.json()
    assert email in payload["activities"][activity_name]["participants"]
    assert email in app_module.activities[activity_name]["participants"]

    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
