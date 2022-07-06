from __future__ import annotations

import json

from pydantic import BaseModel
from typing import Dict, Any


class MenuBase(BaseModel):
    name: str = None
    path: str = None
    meta: Dict[str, Any] = None
    children_ids: str = None

    class Config:
        # allow from_orm
        orm_mode = True


class OutMenu(MenuBase):
    pass


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass
