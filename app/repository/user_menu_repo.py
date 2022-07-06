from typing import Union, Dict, Any, List

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import UserMenuModel
from app.repository.base import RepoBase
from app.schemas import UserMenuUpdate, UserMenuCreate


class UserMenuRepo(RepoBase[UserMenuModel, UserMenuCreate, UserMenuUpdate]):
    def get_by_user_id(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        query_string = text(
            'select m.name,m.path,m.meta,um.id,um.children_ids,um.level,um.menu_order from user_menu um left join menu m on um.menu_id = m.id where um.user_id=:user_id')
        return db.execute(query_string, {'user_id': user_id}).mappings().all()

    def update(self, db: Session, *, db_obj: UserMenuModel, obj_in: Union[UserMenuUpdate, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["menu_id"]:
            return super().update(db, db_obj=db_obj, obj_in=update_data)


user_menu_repo = UserMenuRepo(UserMenuModel)
