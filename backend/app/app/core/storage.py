import os
from pathlib import Path
from typing import Union

from app.core.config import settings
from app.models.data import FolderModel, PlanYmlFileModel


def resolve_folder(full_path: str) -> FolderModel:
    elems = list(filter(None, full_path.split("/")))
    if not elems:
        return FolderModel(
            name=settings.STORAGE_ROOT_DIR_NAME,
            full_path="/",
            is_root=True
        )
    return FolderModel(
        name=elems[-1],
        full_path="/" + "/".join(elems[:-1]),
        is_root=True
    )


def split_root(root_dir: str, current_dir: str) -> tuple[str, str]:
    base_dir, name = os.path.split(current_dir)
    if base_dir.startswith(root_dir):
        base_dir = base_dir[len(root_dir):]
    if not base_dir.startswith("/"):
        base_dir = "/" + base_dir
    return base_dir, name


def get_folders(root_dir: Path) -> list[FolderModel]:
    folders = []
    storage_root_dir = str(settings.STORAGE_DIR)
    for current_dir, dirs, files in os.walk(root_dir, followlinks=settings.STORAGE_FOLLOW_SYMLINKS):
        if current_dir == storage_root_dir:
            name = settings.STORAGE_ROOT_DIR_NAME
            full_path = "/"
            is_root = True
        else:
            full_path, name = split_root(storage_root_dir, current_dir)
            is_root = False
        folders.append(FolderModel(
            name=name,
            full_path=full_path,
            is_root=is_root,
            plan_files=[
                PlanYmlFileModel(name=f_name) for f_name in files if f_name.endswith(".yml")
            ],
        ))

    return folders
