from typing import Any, List

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def read_plans() -> Any:
    return []

