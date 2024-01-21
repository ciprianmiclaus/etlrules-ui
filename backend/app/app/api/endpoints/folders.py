import os
import shutil

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.data import FolderModel
from app.core.storage import get_folders, resolve_folder

router = APIRouter()


@router.get("/folders")
def get_all_folders() -> list[FolderModel]:
    return get_folders(settings.STORAGE_DIR)


@router.get("/folders/{path}")
def get_folder(path: str) -> FolderModel:
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Folder not found")
    return resolve_folder(path)


@router.post("/folders/{path}")
def create_folder(path: str) -> FolderModel:
    path = os.path.join(settings.STORAGE_DIR, path)
    try:
        os.makedirs(path, exist_ok=False)
    except FileExistsError:
        raise HTTPException(status_code=400, detail="Folder already exists")
    except IOError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return resolve_folder(path)


@router.put("/folders/{path}")
def rename_folder(path: str, new_name: str) -> FolderModel:
    local_base_dir, _ = os.path.split(path)
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Folder not found")
    base_dir, _ = os.path.split(path)
    try:
        os.rename(path, os.path.join(base_dir, new_name))
    except IOError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return resolve_folder(os.path.join(local_base_dir, new_name))


@router.delete("/folders/{path}")
def remove_folder(path: str) -> None:
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Folder not found")
    try:
        shutil.rmtree(path)
    except IOError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
