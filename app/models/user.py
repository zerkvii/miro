import enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from datetime import datetime
from app.db.base_class import Base


class ROLE(enum.Enum):
    SUPER_USER = 0
    ADMIN = 1
    USER = 2


# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(64), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    # items = relationship("Item", back_populates="owner")
    avatar = Column(String(256), nullable=True)
    phone = Column(String(128), nullable=True)
    # registrationDate = Colum(String(128), nullable=True)
    registrationDate = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(ROLE), nullable=False, default=ROLE.ADMIN)

    job = Column(String(128), nullable=True)
    organization = Column(String(128), nullable=True)
    location = Column(String(128), nullable=True)
    introduction = Column(String(128), nullable=True)
    personalWebsite = Column(String(128), nullable=True)
    jobName = Column(String(128), nullable=True)
    organizationName = Column(String(128), nullable=True)
    locationName = Column(String(128), nullable=True)
