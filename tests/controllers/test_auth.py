import json
from datetime import datetime, timedelta, timezone
from models.user import User
from models.jwt_token import JWTToken
from sqlmodel import Session, select
from fastapi.testclient import TestClient
from http.cookiejar import Cookie
from tests.fixtures import session_fixture, client_fixture
from config.config import settings
from jwt import decode as jwt_decode


async def test_and_signup(session: Session, client: TestClient):
    response = client.post(
        "/auth/signup",
        json={"name": "JP", "email": "test@test.com", "password": "test_password"},
        headers={"content_type": "application/json"},
    )
    assert response.status_code == 201

    json_string = response.read().decode("utf-8")
    json_dict = json.loads(json_string)
    assert json_dict["email"] == "test@test.com"
    assert json_dict["name"] == "JP"
    assert bool(json_dict["created_at"])
    assert bool(json_dict["updated_at"])
    assert json_dict["active"] is True
    assert json_dict["confirmed_at"] is None

    user = session.exec(select(User).where(User.email == "test@test.com")).first()
    assert user is not None


async def test_and_login(session: Session, client: TestClient):
    user = User(name="JP", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.name == "JP"
    assert user.email == "test@test.com"
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.confirmed_at is None

    await user.encrypt_password("test_password", session)
    password_verified = await user.verify_password("test_password", session)
    assert password_verified

    user = session.exec(select(User).where(User.email == user.email)).first()
    assert user is not None
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "test_password"},
        headers={"content_type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    cookie = response.cookies.get("jwt")
    assert cookie is not None
    payload = jwt_decode(
        cookie, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    username = payload.get("sub")
    assert username == user.email

    json_string = response.read().decode("utf-8")
    json_dict = json.loads(json_string)

    payload = jwt_decode(
        json_dict["access_token"],
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
    username = payload.get("sub")
    assert username == user.email


async def test_and_verify_account_auth(session: Session, client: TestClient):
    user = User(name="JP", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.name == "JP"
    assert user.email == "test@test.com"
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.confirmed_at is None

    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    access_token = JWTToken.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    client.cookies = [("jwt", access_token)]

    cookie = client.cookies.get("jwt")
    assert cookie is not None
    payload = jwt_decode(
        cookie, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    username = payload.get("sub")
    assert username == user.email
    activation_link = user.get_activation_link()
    response = client.get(activation_link)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == str(user.id)
    assert response_data["confirmed_at"] is not None


# TODO add tests for pyotp stuff
