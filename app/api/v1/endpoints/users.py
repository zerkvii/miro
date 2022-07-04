from fastapi import APIRouter, Depends, status

# from app.depends import get_token_header
from app.schemas.model import InUser, OutUser
from app.schemas.response import Response, STATUS
from app.repository import user_repo
from app.db.init_db import get_database, AsyncIOMotorClient
from datetime import timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.jwt import create_access_token, get_current_user_authorizer

router = APIRouter(
    prefix='/users',
    tags=['users'],
    # dependencies=[Depends(get_token_header)],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Not Found'}
    }
)


@router.get('/info')
async def get_user_info(user: OutUser = Depends(get_current_user_authorizer())):
    return Response(status=STATUS.SUCCESS, info='get info successful', data=user)


@router.get('/menu')
async def get_user_menu(user: OutUser = Depends(get_current_user_authorizer()),
                        db: AsyncIOMotorClient = Depends(get_database)):
    menus = await user_repo.get_user_menus(db, user.username)
    return Response(status=STATUS.SUCCESS, info='get info successful', data=menus)


@router.post('/auth')
async def auth_user(user: InUser, db: AsyncIOMotorClient = Depends(get_database)):
    # print(db)
    db_user = await user_repo.get_user(db, user.username)
    if db_user is None:
        return Response(status=STATUS.BAD_REQUEST, info='user not found')
    elif not db_user.check_password(user.password):
        return Response(status=STATUS.BAD_REQUEST, info='pwd not correct')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"username": db_user.username}, expires_delta=access_token_expires
    )
    return Response(status=STATUS.SUCCESS, info='get user successfully', data={'token': token})
