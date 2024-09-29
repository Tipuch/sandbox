from typing import Annotated

from fastapi import Depends
from inertia import Inertia, inertia_dependency_factory
from config.config import settings


InertiaDep = Annotated[
    Inertia, Depends(inertia_dependency_factory(settings.get_inertia_config()))
]
