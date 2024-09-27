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
from config.dev import DevConfig


def get_config():
    if "ENV" not in os.environ:
        return DevConfig()
    else:
        return DevConfig()


config = get_config()

app = FastAPI()
app.add_exception_handler(
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,
)
app.add_exception_handler(
    RequestValidationError,
    inertia_request_validation_exception_handler,
)
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

InertiaDep = Annotated[
    Inertia, Depends(inertia_dependency_factory(config.get_inertia_config()))
]

app.mount("/src", StaticFiles(directory=config.SVELTE_DIR), name="src")
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(config.SVELTE_DIR, "assets")),
    name="assets",
)


@app.get("/", response_model=None)
async def index(inertia: InertiaDep) -> InertiaResponse:
    props = {
        "message": "hello from index",
    }
    return await inertia.render("index", props)
