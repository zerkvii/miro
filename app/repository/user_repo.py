from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.repository.base import RepoBase
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserUpdate


class UserRepo(RepoBase[UserModel, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_username_or_email(self, db: Session, *, username_or_email: str) -> Optional[UserModel]:
        # * is used to force to explicitly pass the email_or_username parameter
        return db.query(UserModel).filter(
            (UserModel.email == username_or_email) | (UserModel.username == username_or_email)
        ).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> UserModel:
        db_obj = UserModel(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: UserModel, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username_or_email: str, password: str) -> Optional[UserModel]:
        query_user = self.get_by_username_or_email(db, username_or_email=username_or_email)
        if not query_user:
            return None
        if not verify_password(password, query_user.hashed_password):
            return None
        return query_user

    def is_active(self, cur_user: UserModel) -> bool:
        return cur_user.is_active

    def is_superuser(self, cur_user: UserModel) -> bool:
        return cur_user.is_superuser


user_repo = UserRepo(UserModel)
