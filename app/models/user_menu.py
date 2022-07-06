from sqlalchemy import Column, Integer, UniqueConstraint, String

from app.db.base_class import Base


class UserMenuModel(Base):
    __tablename__ = 'user_menu'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    menu_id = Column(Integer, nullable=False)
    menu_order = Column(Integer, nullable=True)
    # children_id ref to id not menu_id
    children_ids = Column(String(32), nullable=True)
    level = Column(Integer, nullable=False, default=2)
    UniqueConstraint(user_id, menu_id, name='uix_1')
    # items = relationship("Item", back_populates="owner")
