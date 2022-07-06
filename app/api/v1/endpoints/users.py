from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import repository, models
from app.api import deps
from app.core import security
from app.models import UserModel
from app.schemas.user import InUser, OutUser
from app.schemas.response import Response, STATUS
from app.schemas.user_menu import UserMenuOut

router = APIRouter()


@router.post('/auth')
async def get_auth_token(in_user: InUser, db: Session = Depends(deps.get_db)):
    # user = user_repo.get_by_email_or_username(db, email_or_username=in_user.username)
    user = repository.user_repo.authenticate(db, username_or_email=in_user.username, password=in_user.password)
    if not user:
        return Response(status=STATUS.NOT_FOUND, info='User not found')
    if not repository.user_repo.is_active(user):
        return Response(status=STATUS.TOKEN_EXPIRE, info='User is not active')
    token = security.create_access_token(
        user.id
    )
    return Response(status=STATUS.SUCCESS, info='get token: successful', data={'token': token})


@router.get('/info')
async def get_user_info(current_user: UserModel = Depends(deps.get_current_user)):
    return Response(status=STATUS.SUCCESS, info='get info successful', data=OutUser.from_orm(current_user))


@router.get('/menu')
async def get_user_info(current_user: UserModel = Depends(deps.get_current_user),
                        db: Session = Depends(deps.get_db)):
    menus = repository.user_menu_repo.get_by_user_id(db, user_id=current_user.id)
    menu_list = []
    for menu in menus:
        menu_list.append(UserMenuOut().parse_dict(menu))
    user_menus = traverse_menus(menu_list)
    return Response(status=STATUS.SUCCESS, info='get info successful', data=user_menus)


def traverse_menus(menu_list: List[UserMenuOut]) -> List[UserMenuOut]:
    result = []
    for menu in menu_list:
        if menu.level == 1 and menu.children_ids and menu.children_ids.strip() != '':
            children_ids = [int(e) for e in menu.children_ids.split(',')]
            menu.children = get_sub_menus(menu_list, children_ids)
            result.append(menu)
        elif menu.level == 1:
            result.append(menu)
    return result


def get_sub_menus(menu_list: List[UserMenuOut], children_ids: List[int]) -> List[UserMenuOut]:
    sub_menus = []
    for m in menu_list:
        if m.id in children_ids:
            if m.children_ids is not None and m.children_ids.strip() != '':
                sub_children_ids = [int(e) for e in m.children_ids.split(',')]
                m.children = get_sub_menus(menu_list, sub_children_ids)
            sub_menus.append(m)
    return sub_menus
