from typing import Optional

from pydantic import BaseModel


class PlanYmlFileModel(BaseModel):
    name: str


class FolderModel(BaseModel):
    name: str
    full_path: str
    is_root: bool=False
    plan_files: list[PlanYmlFileModel]
