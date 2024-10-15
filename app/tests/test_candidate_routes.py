from fastapi import status

from app.tests.conftest import client, authenticate, test_db


def test_candidate_list(test_db):
    """
    Test retrieval of the candidate list with valid authentication.
    """
    token = authenticate()

    response = client.get("/candidates", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK


def test_candidate_list_for_anonymous_user():
    """
    Test candidate list retrieval by an unauthenticated user.
    """
    response = client.get("/candidates")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_candidate(test_db):
    """
    Test creation of a new candidate with valid authentication.
    """
    token = authenticate()

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "candidate name",
        "email": "candidate@example.com",
        "phone": "phone number",
    }

    response = client.post("/candidates", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED


def test_create_candidate_with_missing_field(test_db):
    """
    Test candidate creation with missing required fields.
    """
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"name": "candidate name", "email": "candidate@example.com"}
    response = client.post("/candidates", json=payload, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_candidate_with_same_email(test_db):
    """
    Test candidate creation with a duplicate email address.
    """
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "name": "candidate name",
        "email": "candidate@example.com",
        "phone": "phone number",
    }
    # create first
    response = client.post("/candidates", json=payload, headers=headers)
    # create second
    response = client.post("/candidates", json=payload, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_candidate(test_db):
    """
    Test retrieval of a candidate by ID and handling of invalid IDs.
    """
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "candidate name",
        "email": "candidate@example.com",
        "phone": "phone number",
    }
    # create candidate
    response = client.post("/candidates", json=payload, headers=headers)
    candidate_id: str = response.json().get("id")

    response = client.get(f"/candidates/{candidate_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    # test with invalid id
    response = client.get(f"/candidates/invalid-id", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_candidate(test_db):
    """
    Test deletion of a candidate by ID and handling of invalid IDs.
    """
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "candidate name",
        "email": "candidate@example.com",
        "phone": "phone number",
    }
    # create candidate
    response = client.post("/candidates", json=payload, headers=headers)
    candidate_id: str = response.json().get("id")

    response = client.delete(f"/candidates/{candidate_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    # test with invalid id
    response = client.delete(f"/candidates/invalid-id", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_generate_candidate_report(test_db):
    """
    Test generation of a candidate report with valid authentication.
    """
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(url="/candidates/generate-report/", headers=headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
