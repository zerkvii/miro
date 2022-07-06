from typing import Union, Dict, Any, List

from sqlalchemy.orm import Session

from app.models import MenuModel
from app.repository.base import RepoBase
from app.schemas.menu import MenuCreate, MenuUpdate
from sqlalchemy import text


class MenuRepo(RepoBase[MenuModel, MenuCreate, MenuUpdate]):

    # def get_by_menu_level(self, db: Session, *, menu_level: int):
    #     query_string = text("SELECT menu.id FROM menu WHERE level=:level")
    #     ret = db.execute(query_string, {'level': menu_level}).mappings().all()
    #     return list(ret)
    def get_all_menus(self, db):
        ret = db.query(MenuModel).all()
        return ret

    def get_by_menu_name(self, db: Session, *, menu_name):
        menu = db.query(MenuModel).filter(MenuModel.name == menu_name).first()
        return menu

    # def get_by_user_id(self, db: Session, *, user_id: int):
    #     query_string = text(
    #         "SELECT menu.*,um.menu_order FROM menu LEFT JOIN user_menu um ON menu.id = um.menu_id WHERE um.user_id =:user_id")
    #     ret = db.execute(query_string, {'user_id': user_id}).mappings().all()
    #     return list(ret)
    #
    # def get_by_children_ids(self, db: Session, *, children_ids: str):
    #     ids = list(int(c) for c in children_ids.split(','))
    #     query_string = text("SELECT * FROM menu WHERE id IN :children_ids")
    #     ret = db.execute(query_string, {'children_ids': ids}).mappings().all()
    #     return list(ret)

    def update(self, db: Session, *, db_obj: MenuModel, obj_in: Union[MenuUpdate, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["meta"]:
            return super().update(db, db_obj=db_obj, obj_in=update_data)


menu_repo = MenuRepo(MenuModel)
