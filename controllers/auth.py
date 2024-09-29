from fastapi import APIRouter
from inertia import InertiaResponse

from dependencies.inertia import InertiaDep

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/signup", response_model=None)
async def get_signup(inertia: InertiaDep) -> InertiaResponse:
    props = {
        "message": "hello from index",
    }
    return await inertia.render("auth/signup", props)  # noqa: F821
