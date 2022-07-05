from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(64), nullable=False)
    name = Column(String(64), index=True, nullable=False)
    meta = Column(String(128), nullable=True)
    children = Column(String(128), nullable=True)


class UserMenu(Base):
    __tablename__ = 'user_menu'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    menu_id = Column(Integer, nullable=False)
    # items = relationship("Item", back_populates="owner")
