from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/signup")
async def get_signup():
    pass
