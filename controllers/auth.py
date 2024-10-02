from fastapi import APIRouter, Depends, HTTPException
from inertia import InertiaResponse
from sqlmodel import Session, select

from db import get_session
from dependencies.inertia import InertiaDep
from models.user import User, UserCreate, UserRead

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
    db_new_user.encrypt_password(new_user.password)

    return db_new_user


@router.get("/signup/success", response_model=None)
async def get_signup_success(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render("auth/signup_success", {})
