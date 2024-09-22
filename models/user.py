from argon2 import PasswordHasher
import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, default="")
    password: str = Field(default="")
    active: bool = Field(default=True)

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
