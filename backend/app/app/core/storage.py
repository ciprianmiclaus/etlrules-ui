from etlrules import Plan
import os

from app.core.config import settings
from app.models.data import FolderModel, PlanYmlFileModel, PlanModel


def get_folder_by_path(path: str) -> FolderModel:
    path_components = list(filter(None, path.split("/")))
    storage_root_dir = str(settings.STORAGE_DIR)
    return get_folder(
        full_local_path=os.path.join(storage_root_dir, *path_components),
        relative_path="/" + "/".join(path_components),
        name=path_components[-1] if path_components else settings.STORAGE_ROOT_DIR_NAME
    )


def get_folder(full_local_path: str, relative_path: str, name: str) -> FolderModel:
    sub_folders = []
    plan_files = []
    for entry in os.scandir(full_local_path):
        if entry.is_file():
            plan_files.append(
                PlanYmlFileModel(name=entry.name)
            )
        elif entry.is_dir():
            sub_folders.append(
                get_folder(
                    full_local_path=os.path.join(full_local_path, entry.name),
                    relative_path=os.path.join(relative_path, entry.name),
                    name=entry.name
                )
            )
    return FolderModel(
        name=name,
        full_path=relative_path,
        sub_folders=sub_folders,
        plan_files=plan_files
    )


def write_plan(path: str, plan: PlanModel) -> None:
    plan_instance = Plan.from_dict(plan, settings.ETLRULES_BACKEND)
    yml = plan_instance.to_yaml()
    with open(path, encoding="utf-8") as f:
        f.write(yml)
