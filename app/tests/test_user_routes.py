from fastapi import status

from app.tests.conftest import test_db, client, create_test_user


def test_user_register(test_db):
    request_body = {'email': 'admin1@gmail.com', 'password': 'admin'}
    response = client.post(url='/users/register/', json=request_body)

    assert response.status_code == status.HTTP_201_CREATED

    request_body = {'email': 'admin1@gmail.com', 'password': 'admin'}
    response = client.post(url='/users/register/', json=request_body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_register_with_missing_field(test_db):
    request_body = {'email': 'newuser@gmail.com'}
    response = client.post(url='/users/register/', json=request_body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_user_login_with_valid_credentials(test_db):
    # create user first
    create_test_user()

    request_body = {'email': 'admin@gmail.com', 'password': 'admin'}

    response = client.post(url='/users/login/', json=request_body)

    assert response.status_code == status.HTTP_200_OK


def test_user_login_with_invalid_credentials(test_db):
    request_body = {'email': 'admin@gmail.com', 'password': 'admin'}

    request_body.update({'password': 'wrong-password'})
    login_response = client.post(url='/users/login/', json=request_body)

    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
