from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import repository, models
from app.api import deps
from app.core import security
from app.schemas import OutMenu
from app.schemas.user import InUser, OutUser
from app.schemas.response import Response, STATUS

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
async def get_user_info(current_user: models.user = Depends(deps.get_current_user)):
    return Response(status=STATUS.SUCCESS, info='get info successful', data=OutUser().from_user_model(current_user))


@router.get('/menu')
async def get_user_info(current_user: models.user = Depends(deps.get_current_user),
                        db: Session = Depends(deps.get_db)):
    menus = repository.menu_repo.get_by_user_id(db, user_id=current_user.id)
    menu_list = []
    for menu in menus:
        if menu.children is not None:
            sub_menu = repository.menu_repo.get_by_children_ids(db, children_ids=menu.children)
            out_menu = OutMenu().from_menu_model(menu)
            out_menu.children = sub_menu
            menu_list.append(out_menu)
        else:
            menu_list.append(OutMenu().from_menu_model(menu))
    return Response(status=STATUS.SUCCESS, info='get info successful', data=menu_list)
