import os

from fastapi.templating import Jinja2Templates
from inertia import InertiaConfig


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]

    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

    MANIFEST_JSON = os.path.join(
        os.path.dirname(__file__), "static", "dist", "manifest.json"
    )

    SVELTE_DIR = os.path.join(os.path.dirname(__file__), "static", "src")

    def get_templates(self):
        return Jinja2Templates(directory=self.TEMPLATES_DIR)

    def get_inertia_config(self) -> InertiaConfig:
        raise NotImplementedError()
