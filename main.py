import os
from fastapi.exceptions import RequestValidationError
from inertia import (
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,
    InertiaResponse,
    inertia_request_validation_exception_handler,
)
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from config.config import settings
from dependencies.inertia import InertiaDep
from controllers import auth


app = FastAPI()
app.add_exception_handler(
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,  # type: ignore
)
app.add_exception_handler(
    RequestValidationError,
    inertia_request_validation_exception_handler,  # type: ignore
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.include_router(auth.router)
app.mount("/src", StaticFiles(directory=settings.SVELTE_DIR), name="src")
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(settings.SVELTE_DIR, "assets")),
    name="assets",
)


@app.get("/", response_model=None)
async def index(inertia: InertiaDep) -> InertiaResponse:
    props = {
        "message": "hello from index",
    }
    return await inertia.render("index", props)
