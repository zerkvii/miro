from fastapi import Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models import Menu, UserMenu
from app.repository.base import RepoBase
from app.schemas.menu import MenuCreate, MenuUpdate, OutMenu
from sqlalchemy import text


class MenuRepo(RepoBase[Menu, MenuCreate, MenuUpdate]):
    def get_by_user_id(self, db: Session, *, user_id):
        query_string = text("SELECT * FROM menu WHERE id IN (SELECT menu_id FROM user_menu WHERE user_id = :user_id)")
        ret = db.execute(query_string, {'user_id': user_id})
        return list(ret)

    def get_by_children_ids(self, db: Session, *, children_ids):
        ids = list(int(c) for c in children_ids.split(','))
        query_string = text("SELECT * FROM menu WHERE id IN :children_ids")
        ret = db.execute(query_string, {'children_ids': ids})
        sub_menu_list = []
        for sub_menu in ret:
            sub_menu_list.append(OutMenu().from_menu_model(sub_menu))
        return sub_menu_list


menu_repo = MenuRepo(Menu)
