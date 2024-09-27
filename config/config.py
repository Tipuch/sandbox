import os

from fastapi.templating import Jinja2Templates
from inertia import InertiaConfig
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    TEMPLATES_DIR = Path("./templates").resolve()

    MANIFEST_JSON = Path("./static/dist/manifest.json").resolve()
    SVELTE_DIR = Path("./static/src").resolve()

    def get_templates(self):
        return Jinja2Templates(directory=self.TEMPLATES_DIR)

    def get_inertia_config(self) -> InertiaConfig:
        raise NotImplementedError()
