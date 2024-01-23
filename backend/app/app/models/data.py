from typing import Optional

from pydantic import BaseModel


class PlanYmlFileModel(BaseModel):
    name: str


class FolderModel(BaseModel):
    name: str
    full_path: str
    sub_folders: list['FolderModel']
    plan_files: list[PlanYmlFileModel]


class PlanModel(BaseModel):
    name: Optional[str]
    description: Optional[str]=None
    context: Optional[dict]=None
    strict: bool=True
    rules: list[dict]
