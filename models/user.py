from typing import Optional
import uuid
from datetime import datetime
from config.config import settings

from argon2 import PasswordHasher
from sqlmodel import Field, SQLModel
from itsdangerous import URLSafeTimedSerializer


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    name: str = Field(index=True)
    email: str = Field(unique=True, default="")
    password: str = Field(default="")
    active: bool = Field(default=False, nullable=False)
    confirmed_at: Optional[datetime] = Field(default=None, nullable=True)

    def encrypt_password(self, raw_password: str) -> str:
        password_hasher = PasswordHasher()
        hash = password_hasher.hash(raw_password)
        self.password = hash
        return hash

    def verify_password(self, raw_password: str) -> bool:
        password_hasher = PasswordHasher()
        verified = password_hasher.verify(self.password, raw_password)
        if not verified:
            return False
        if password_hasher.check_needs_rehash(self.password):
            self.encrypt_password(raw_password)
        return True

    def get_activation_link(self) -> str:
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="activate")
        return ""
