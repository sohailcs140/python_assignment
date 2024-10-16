from fastapi import status

from app.tests.conftest import test_db, client, authenticate


def test_create_skill(test_db):
    """
    Test creation of a new skill associated with a candidate.
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
    candidate_id = response.json().get("id")

    skill_payload = {"name": "skill name", "candidate_id": candidate_id}

    # create skill
    response = client.post("/skills", json=skill_payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED


def test_retrieve_skill(test_db):
    """
    Test retrieval of a skill by its ID.
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
    candidate_id = response.json().get("id")

    skill_payload = {"name": "skill name", "candidate_id": candidate_id}

    # create skill
    response = client.post("/skills", json=skill_payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    skill_id = response.json().get("id")
    #     retrieve a skill
    response = client.get(f"/skills/{skill_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK


def test_delete_skill(test_db):
    """
    Test deletion of a skill by its ID.
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
    candidate_id = response.json().get("id")

    skill_payload = {"name": "skill name", "candidate_id": candidate_id}

    # create skill
    response = client.post("/skills", json=skill_payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    skill_id = response.json().get("id")

    #     retrieve a skill
    response = client.delete(f"/skills/{skill_id}/delete", headers=headers)

    assert response.status_code == status.HTTP_200_OK
