import argon2
import pyotp
import arrow
from typing import Optional, Self, Tuple
import uuid
from datetime import datetime, timedelta, timezone

from config.config import settings

from argon2 import PasswordHasher
from sqlmodel import Field, SQLModel, select
from itsdangerous import BadSignature, URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired

from db import get_session


class UserCreate(SQLModel):
    name: str = Field(max_length=500)
    email: str = Field(max_length=500)
    password: str = Field(max_length=250)


class UserRead(SQLModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    name: str = Field(max_length=500)
    email: str = Field(max_length=500)
    active: bool
    confirmed_at: Optional[datetime]


class UserPyotpSecret(UserRead):
    pyotp_secret: str = Field(default="", max_length=500, nullable=False)
    pyotp_uri: str = ""


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    name: str = Field(index=True, max_length=500, nullable=False)
    email: str = Field(unique=True, max_length=500, nullable=False)
    password: str = Field(default="", max_length=250, nullable=False)
    active: bool = Field(default=True, nullable=False)
    confirmed_at: Optional[datetime] = Field(default=None, nullable=True)
    pyotp_secret: str = Field(default="", max_length=500, nullable=False)
    pyotp_last_auth_at: Optional[datetime] = Field(default=None, nullable=True)

    @classmethod
    async def authenticate_user(
        cls, email: str, password: str
    ) -> Tuple[Optional[Self], bool]:  # type: ignore
        """
        returns user and if the user has pyotp enabled or not
        """
        async for session in get_session():
            user = session.exec(select(cls).where(cls.email == email)).first()
            if not user:
                return (None, False)
            elif user.pyotp_secret:
                print("testing pyotp")
                otp = password[-6:]
                password = password[:-6]
                password_verified = await user.verify_password(password)
                otp_verified = await user.verify_pyotp(otp)
                if password_verified and otp_verified:
                    return (user, True)
                else:
                    return (None, False)
            elif await user.verify_password(password):
                print("testing only username & password")
                return (user, False)
            return (None, False)

    async def encrypt_password(self, raw_password: str) -> str:
        password_hasher = PasswordHasher()
        hash = password_hasher.hash(raw_password)
        self.password = hash
        async for session in get_session():
            session.add(self)
            session.commit()
            session.refresh(self)
        return hash

    async def verify_password(self, raw_password: str) -> bool:
        password_hasher = PasswordHasher()
        verified = False
        try:
            verified = password_hasher.verify(self.password, raw_password)
        except argon2.exceptions.VerifyMismatchError:
            return False
        if not verified:
            return False
        if password_hasher.check_needs_rehash(self.password):
            await self.encrypt_password(raw_password)
        return True

    def get_activation_link(self) -> str:
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="activate")
        return f"/auth/activate/{serializer.dumps(str(self.id))}"

    async def activate(self, token: str) -> bool:
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="activate")
        valid = False
        try:
            retrieved_id = serializer.loads(token, max_age=settings.ACTIVATION_MAX_AGE)
            if str(self.id) != retrieved_id:
                raise BadSignature(
                    f"ids do not match, expected {self.id} got {retrieved_id}"
                )
            self.confirmed_at = datetime.now(timezone.utc)
            async for session in get_session():
                obj_session = session.object_session(self)
                if obj_session:
                    obj_session.add(self)
                    obj_session.commit()
                    obj_session.refresh(self)
                else:
                    session.add(self)
                    session.commit()
                    session.refresh(self)
            valid = True
        except (BadSignature, SignatureExpired):
            valid = False

        return valid

    async def set_pyotp_secret(self) -> str:
        secret = pyotp.random_base32()
        self.pyotp_secret = secret
        return secret

    async def verify_pyotp(self, otp: str) -> bool:
        if not self.pyotp_secret:
            return False
        totp = pyotp.TOTP(self.pyotp_secret, interval=settings.PYTOP_INTERVAL)
        last_interval = arrow.utcnow() - timedelta(seconds=settings.PYTOP_INTERVAL)
        # here we check to avoid replayability of last valid token

        if (
            self.pyotp_last_auth_at
            and arrow.get(self.pyotp_last_auth_at, "UTC") >= last_interval
        ):
            return False

        if totp.verify(otp):
            self.pyotp_last_auth_at = datetime.now(timezone.utc)

            async for session in get_session():
                obj_session = session.object_session(self)
                if obj_session:
                    obj_session.add(self)
                    obj_session.commit()
                    obj_session.refresh(self)
                else:
                    session.add(self)
                    session.commit()
                    session.refresh(self)
            return True
        return False
