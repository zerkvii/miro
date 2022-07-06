from typing import TYPE_CHECKING, Dict, Any
# from sqlalchemy import UniqueConstraint
from sqlalchemy import Boolean, Column, Integer, String, JSON, ARRAY
from sqlalchemy.dialects.mysql import SET
from sqlalchemy.orm import relationship
import json
from app.db.base_class import Base


# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class MenuModel(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(64), nullable=False, unique=True)
    name = Column(String(64), index=True, nullable=False, unique=True)
    # preset father_id
    children_ids = Column(String(32), nullable=True)
    meta = Column(JSON, nullable=True)
