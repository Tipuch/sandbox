from typing import Dict, Optional
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.config import settings
from jwt import InvalidTokenError, decode as jwt_decode
from db import get_session
from models.jwt_token import JWTTokenData
from models.user import User
from sqlmodel import Session, select


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    """
    This class allows to not only fetch the jwt token from the headers
    but also from a cookie, in case we want to use a secure cookie to store the jwt on the
    frontend
    """

    def get_jwt_cookie(self, cookies: Dict[str, str]):
        jwt = cookies.get("jwt")
        if not jwt and self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return jwt

    async def __call__(self, request: Request) -> Optional[str]:
        try:
            jwt = await super().__call__(request)
            if not jwt:
                jwt = self.get_jwt_cookie(request.cookies)
        except HTTPException:
            jwt = self.get_jwt_cookie(request.cookies)
        return jwt


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = JWTTokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(User).where(User.email == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
