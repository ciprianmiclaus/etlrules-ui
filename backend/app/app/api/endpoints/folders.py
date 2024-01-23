import os
import shutil

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.data import FolderModel
from app.core.storage import get_folder_by_path

router = APIRouter()


@router.get("/folders")
def get_all_folders() -> list[FolderModel]:
    return [get_folder_by_path("/")]


@router.get("/folders/{path}")
def get_folder(path: str) -> FolderModel:
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Folder not found")
    return get_folder_by_path(path)


@router.post("/folders/{path}")
def create_folder(path: str) -> FolderModel:
    local_full_path = os.path.join(settings.STORAGE_DIR, path)
    try:
        os.makedirs(local_full_path, exist_ok=False)
    except FileExistsError:
        raise HTTPException(status_code=400, detail="Folder already exists")
    except IOError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return get_folder_by_path(path)


@router.put("/folders/{path}")
def rename_folder(path: str, new_name: str) -> FolderModel:
    local_base_dir, _ = os.path.split(path)
    local_full_path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(local_full_path) or not os.path.isdir(local_full_path):
        raise HTTPException(status_code=404, detail="Folder not found")
    local_base_dir, _ = os.path.split(local_full_path)
    base_dir, _ = os.path.split(path)
    try:
        os.rename(path, os.path.join(local_base_dir, new_name))
    except IOError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return get_folder_by_path(os.path.join(base_dir, new_name))


@router.delete("/folders/{path}")
def remove_folder(path: str) -> None:
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Folder not found")
    try:
        shutil.rmtree(path)
    except IOError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
