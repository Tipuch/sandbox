import os
from typing import Annotated
from fastapi.exceptions import RequestValidationError
from inertia import (
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,
    Inertia,
    inertia_dependency_factory,
    InertiaResponse,
    inertia_request_validation_exception_handler,
)
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Depends
from config.config import settings

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

InertiaDep = Annotated[
    Inertia, Depends(inertia_dependency_factory(settings.get_inertia_config()))
]

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
