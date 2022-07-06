from __future__ import annotations
import json
from typing import Dict, Any, List

from pydantic import BaseModel


class UserMenuBase(BaseModel):
    id: int = None
    user_id: int = None
    menu_id: int = None
    menu_order: int = None
    level: int = None
    children_ids: str = None

    class Config:
        orm_mode = True


class UserMenuCreate(UserMenuBase):
    pass


class UserMenuUpdate(UserMenuBase):
    pass


class UserMenuOut(UserMenuBase):
    name: str = None
    path: str = None
    meta: str = None
    children: List[UserMenuOut] = None

    def parse_dict(self, item: Dict[str, Any]):
        self.id = item['id']
        self.name = item['name']
        self.path = item['path']
        self.children_ids = item['children_ids']
        self.meta = json.loads(item['meta'])
        self.level = item['level']
        self.menu_order = item['menu_order']
        return self
