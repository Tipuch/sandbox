from models.user import User
from sqlmodel import Session
from main import app
from db import get_session
import pyotp
from config.config import settings
from tests.fixtures import session_fixture


async def test_set_and_verify_password(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    user = User(name="JP", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    await user.encrypt_password("test_password", session)

    password_verified = await user.verify_password("test_password", session)
    invalid_password = await user.verify_password("invalid_password", session)
    assert user.id is not None
    assert user.name == "JP"
    assert user.email == "test@test.com"
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.confirmed_at is None
    assert len(user.password) > len("test_password")
    assert user.password != "test_password"
    assert password_verified is True
    assert invalid_password is False


async def test_and_verify_account(session: Session):
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

    activation_link = user.get_activation_link()
    token = activation_link.split("/")[-1]
    activated = await user.activate(token, session)

    assert activated is True
    assert user.confirmed_at is not None


async def test_and_set_pyotp(session: Session):
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

    user.set_pyotp_secret()
    totp = pyotp.TOTP(user.pyotp_secret, interval=settings.PYOTP_INTERVAL)
    otp = totp.now()
    assert await user.verify_pyotp(otp, session)
