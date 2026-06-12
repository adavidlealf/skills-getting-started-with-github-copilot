from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activities = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Swim Club", "Art Club", "Drama Society", "Science Olympiad", "Debate Team"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert set(payload.keys()) == expected_activities
    assert "Chess Club" in payload
    assert isinstance(payload["Chess Club"], dict)
    assert "participants" in payload["Chess Club"]
    assert "michael@mergington.edu" in payload["Chess Club"]["participants"]


def test_signup_for_activity_succeeds():
    # Arrange
    activity_name = "Chess Club"
    new_student_email = "test_student@mergington.edu"
    request_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(request_path, params={"email": new_student_email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {new_student_email} for {activity_name}"


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    request_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(request_path, params={"email": "student@mergington.edu"})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"
    request_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(request_path, params={"email": existing_email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"
