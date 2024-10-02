from sqlmodel import SQLModel
from datetime import datetime, timezone, timedelta
from config.config import settings
import jwt


class JWTToken(SQLModel):
    access_token: str
    token_type: str

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt


class JWTTokenData(SQLModel):
    username: str | None = None
