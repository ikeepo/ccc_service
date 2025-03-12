import json
from pathlib import Path

from fastapi import APIRouter

# from app.api import crud
from app.models.pydantic import CategoryPayloadSchema, CategoryResponseSchema

# from typing import List

# , HTTPException

# from app.models.tortoise import SummarySchema

router = APIRouter()


def load_category_from_json():
    """赶时间, 先这么偷懒"""
    fp_file = Path(__file__)
    fp_json = fp_file.parent / "binance_spot_currency_zone_map.json"
    with open(fp_json, "r") as f:
        data = json.load(f)
    return data


@router.post("/", response_model=CategoryResponseSchema, status_code=201)
async def get_category(payload: CategoryPayloadSchema) -> CategoryResponseSchema:
    data = load_category_from_json()
    base_upper = payload.base.strip().upper()
    category = data.get(
        base_upper,
        "thank you for use ccc, it's under development, report here https://github.com/ikeepo/ccc",
    )
    response_object = {"base": base_upper, "category": category}
    return response_object
