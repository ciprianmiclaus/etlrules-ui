from etlrules import Plan
from fastapi import APIRouter, HTTPException
import os

from app.core.config import settings
from app.models.data import PlanModel
from app.core.storage import write_plan

router = APIRouter()


@router.get("/plans/{path}")
def get_plan(path: str) -> PlanModel:
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Plan not found")
    with open(path, encoding="utf-8") as f:
        yml = f.read()
    plan = Plan.from_yaml(yml, settings.ETLRULES_BACKEND)
    return PlanModel(plan.to_dict())


@router.post("/plans/{path}")
def create_plan(path: str, plan: PlanModel) -> PlanModel:
    path = os.path.join(settings.STORAGE_DIR, path)
    if os.path.exists(path):
        raise HTTPException(status_code=404, detail="Plan already exists")
    try:
        write_plan(path, plan)
    except IOError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return plan


@router.put("/plans/{path}")
def save_plan(path: str, plan: PlanModel) -> PlanModel:
    path = os.path.join(settings.STORAGE_DIR, path)
    try:
        write_plan(path, plan)
    except IOError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return plan


@router.delete("/plans/{path}")
def delete_plan(path: str) -> None:
    path = os.path.join(settings.STORAGE_DIR, path)
    if not os.path.exists(path) or not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Plan not found")
    try:
        os.remove(path)
    except IOError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
