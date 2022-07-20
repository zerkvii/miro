from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from redis.client import Redis
from sqlalchemy.orm import Session

from app import repository
from app.api import deps
from app.core import security
from app.models import UserModel
from app.schemas.user import InUser, OutUser, UserBase
from app.schemas.response import Response, STATUS
from app.schemas.user_menu import UserMenuOut
from app.services.db import get_db
from app.services.redis import get_redis_conn
from app.services import qiniu

router = APIRouter()


@router.post('/auth')
async def get_auth_token(in_user: InUser, db: Session = Depends(get_db), redis: Redis = Depends(get_redis_conn)):
    # user = user_repo.get_by_email_or_username(db, email_or_username=in_user.username)
    user = repository.user_repo.authenticate(db, redis, username_or_email=in_user.username, password=in_user.password)
    if not user:
        return Response(status=STATUS.NOT_FOUND, info='User not found')
    if not repository.user_repo.is_active(redis, user):
        return Response(status=STATUS.TOKEN_EXPIRE, info='User is not active')
    token = security.create_access_token(
        user.id
    )
    return Response(status=STATUS.SUCCESS, info='get token: successful', data={'token': token})


@router.get('/info')
async def get_user_info(current_user: UserModel = Depends(deps.get_current_user)):
    return Response(status=STATUS.SUCCESS, info='get info successful', data=OutUser.from_orm(current_user))


@router.post('/logout')
async def get_user_info(current_user: UserModel = Depends(deps.get_current_user)):
    current_user.is_active = False
    return Response(status=STATUS.SUCCESS, info='logout successful')


@router.get('/menu')
async def get_user_info(current_user: UserModel = Depends(deps.get_current_user),
                        db: Session = Depends(get_db)):
    menus = repository.user_menu_repo.get_by_user_id(db, user_id=current_user.id)
    menu_list = []
    for menu in menus:
        menu_list.append(UserMenuOut().parse_dict(menu))
        # print(menu)
    # user_menus = traverse_menus(menu_list)
    # print(user_menus)
    return Response(status=STATUS.SUCCESS, info='get info successful', data=menu_list)


@router.get('/logo')
async def get_logo():
    logo_url = qiniu.generate_access_url(file='miro/pics/logo.png')
    return Response(status=STATUS.SUCCESS, info='get logo successful', data={'logoUrl': logo_url})


def traverse_menus(menu_list: List[UserMenuOut]) -> List[UserMenuOut]:
    result = []
    for menu in menu_list:
        if menu.level == 1 and menu.children_ids and menu.children_ids.strip() != '':
            children_ids = [int(e) for e in menu.children_ids.split(',')]
            menu.children = get_sub_menus(menu_list, children_ids)
            print(menu.children)
            result.append(menu)
        elif menu.level == 1:
            result.append(menu)
    return result


def get_sub_menus(menu_list: List[UserMenuOut], children_ids: List[int]) -> List[UserMenuOut]:
    sub_menus = []
    print(len(menu_list))
    for m in menu_list:
        if m.id in children_ids:
            print(m)
            if m.children_ids is not None and m.children_ids.strip() != '':
                sub_children_ids = [int(e) for e in m.children_ids.split(',')]
                m.children = get_sub_menus(menu_list, sub_children_ids)
            sub_menus.append(m)
    return sub_menus
