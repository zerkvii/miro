from fastapi import APIRouter
from typing import Optional

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


