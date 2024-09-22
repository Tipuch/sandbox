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
    InertiaConfig,
)
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from config.dev import DevConfig


template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)


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
app.add_middleware(SessionMiddleware, secret_key="secret_key")

manifest_json = os.path.join(
    os.path.dirname(__file__), "static", "dist", "manifest.json"
)

inertia_config = InertiaConfig(
    templates=templates,
    manifest_json_path=manifest_json,
    environment="development",
    use_flash_messages=True,
    use_flash_errors=True,
    entrypoint_filename="main.js",
    assets_prefix="/src",
)

InertiaDep = Annotated[Inertia, Depends(inertia_dependency_factory(inertia_config))]

svelte_dir = os.path.join(os.path.dirname(__file__), "static", "src")

app.mount("/src", StaticFiles(directory=svelte_dir), name="src")
app.mount(
    "/assets", StaticFiles(directory=os.path.join(svelte_dir, "assets")), name="assets"
)


@app.get("/", response_model=None)
async def index(inertia: InertiaDep) -> InertiaResponse:
    props = {
        "message": "hello from index",
    }
    return await inertia.render("index", props)
