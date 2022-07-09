import json

from sqlalchemy.orm import Session

from app import repository, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.db.session import SessionLocal
from app.schemas import UserMenuCreate, MenuUpdate
from app.schemas import MenuCreate


def import_routes(db: Session):
    with open('routes.json') as f:
        routes = json.loads(f.read())
        print(f'import {len(routes)} routes start -----')
        for r in routes:
            if 'name' in r:
                menu = repository.menu_repo.get_by_menu_name(db, menu_name=r['name'])
                if not menu:
                    menu = MenuCreate.parse_obj(r)
                    repository.menu_repo.create(db=db, obj_in=menu)
            else:
                print(r)
        for r in routes:
            if 'children' in r:
                father_menu = repository.menu_repo.get_by_menu_name(db, menu_name=r['name'])
                children_list = []
                for child in r['children']:
                    child_menu = repository.menu_repo.get_by_menu_name(db, menu_name=child['name'])
                    children_list.append(str(child_menu.id))
                update_menu = MenuUpdate.from_orm(father_menu)
                update_menu.children_ids = ','.join(children_list)
                update_ret = repository.menu_repo.update(db, db_obj=father_menu, obj_in=update_menu)
                # for child in r['children']:
                #     child_menu = repository.menu_repo.get_by_menu_name(db, menu_name=child['name'])
                #     update_menu = MenuUpdate.from_orm(child_menu)
                #     update_menu.father_id = cur_father.id
                #     ret = repository.menu_repo.update(db, db_obj=child_menu, obj_in=update_menu)
                #     print(ret)


def init_superuser(db: Session):
    user = repository.user_repo.get_by_email(db, email='233@qq.com')
    if not user:
        user_in = schemas.UserCreate(
            # email=settings.FIRST_SUPERUSER,
            email='233@qq.com',
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username='zerk',
            # password=settings.FIRST_SUPERUSER_PASSWORD,
            # username=settings.FIRST_SUPERUSER_NAME,
        )
        user = repository.user_repo.create(db, obj_in=user_in)  # noqa: F841


def init_superuser_route(db: Session):
    user = repository.user_repo.get_by_email(db, email='zerkvii@gmail.com')
    menus = repository.menu_repo.get_all_menus(db)
    if menus:
        order = 0
        for m in menus:
            user_menu = UserMenuCreate.from_orm(m)
            user_menu.id = None
            user_menu.user_id = user.id
            user_menu.menu_id = m.id
            user_menu.menu_order = order
            if user_menu.children_ids != '':
                user_menu.children_ids = ','.join([str(int(e) + 27) for e in user_menu.children_ids.split(',')])
            if str(m.name).islower():
                user_menu.level = 1
            else:
                user_menu.level = 2
            order += 1
            repository.user_menu_repo.create(db, obj_in=user_menu)


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    # import_routes(db)
    init_superuser(db)
    init_superuser_route(db)
