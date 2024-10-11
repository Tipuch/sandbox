from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from inertia import InertiaResponse
from pyotp import totp
from sqlmodel import Session, select

from config.config import settings
from db import get_session
from dependencies.inertia import InertiaDep
from dependencies.auth import get_current_active_user
from models.jwt_token import JWTToken
from models.user import User, UserCreate, UserRead, UserPyotpSecret

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/signup", response_model=None)
async def get_signup(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render("auth/signup", {})


@router.post("/signup", response_model=UserRead, status_code=201)
async def signup(new_user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.email == new_user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=422, detail="A user with this email already exists."
        )
    db_new_user = User.model_validate(new_user)
    await db_new_user.encrypt_password(new_user.password)

    return db_new_user


@router.get("/signup/success", response_model=None)
async def get_signup_success(
    inertia: InertiaDep, current_user: User = Depends(get_current_active_user)
) -> InertiaResponse:
    activation_link = current_user.get_activation_link()
    current_user_read = UserRead.model_validate(current_user)
    confirmed = bool(current_user_read.confirmed_at)
    return await inertia.render(
        "auth/signup_success",
        {
            "current_user": current_user_read,
            "activation_link": activation_link,
            "confirmed": confirmed,
        },
    )


@router.get("/activate/{activation_token}", response_model=UserRead, status_code=200)
async def activate(
    activation_token: str, current_user: User = Depends(get_current_active_user)
):
    success = await current_user.activate(activation_token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect activation token",
        )
    return current_user


@router.post("/token", response_model=JWTToken, status_code=200)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    authenticated_user, uses_otp = await User.authenticate_user(
        form_data.username, form_data.password
    )
    if not authenticated_user:
        if not uses_otp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password or missing or incorrect OTP",
                headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    access_token = JWTToken.create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="jwt",
        value=access_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=(datetime.now(timezone.utc) + access_token_expires),
    )
    return JWTToken(access_token=access_token, token_type="bearer")


@router.get("/otp/setup", response_model=None)
async def setup_otp(
    inertia: InertiaDep, current_user: User = Depends(get_current_active_user)
) -> InertiaResponse:
    has_active_otp = bool(current_user.pyotp_secret)
    return await inertia.render("auth/otp_setup", {"has_active_otp": has_active_otp})


@router.post("/otp/setup/{otp}", response_model=UserPyotpSecret, status_code=200)
async def save_otp(
    otp: str,
    user_pyotp: UserPyotpSecret,
    current_user: User = Depends(get_current_active_user),
):
    if current_user.id != user_pyotp.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="current_user id and pyotp_user id are different",
        )

    current_user.pyotp_secret = user_pyotp.pyotp_secret
    if not current_user.verify_pyotp(otp):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="OTP invalid.")

    return current_user


@router.get("/otp", response_model=UserPyotpSecret, status_code=200)
async def get_otp(current_user: User = Depends(get_current_active_user)):
    await current_user.set_pyotp_secret()
    current_user_read = UserPyotpSecret.model_validate(current_user)
    current_user_read.pyotp_uri = totp.TOTP(
        current_user_read.pyotp_secret
    ).provisioning_uri(name=current_user_read.email, issuer_name="Sandbox App")
    return current_user_read
