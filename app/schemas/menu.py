from __future__ import annotations

import json

from pydantic import BaseModel
from typing import List, Dict, Any

from app import models


class MenuBase(BaseModel):
    name: str = None
    path: str = None
    children: List[MenuBase] = []
    meta: Dict[str, Any] = None


class OutMenu(MenuBase):
    def from_menu_model(self, model: models.menu):
        self.name = model.name
        self.path = model.path
        if model.meta:
            self.meta = json.loads(model.meta)
        return self


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass
