import json
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from redis.client import Redis

from app import schemas
from app.core import security
from app.core.config import settings
from app.models import UserModel
from app.redis.redis_base import hget_key
from app.schemas import TokenPayload
from app.schemas.response import Response, STATUS
from app.services.redis import get_redis_conn

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(con: Redis = Depends(get_redis_conn), *,
                     token: str = Depends(reusable_oauth2)
                     ) -> Union[UserModel, None]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_str = hget_key(con, settings.ACTIVE_USERS_INFO, str(token_data.sub))
    if not user_str:
        raise HTTPException(status_code=200, detail={"status": 403, "info": "User not found"})
    return UserModel(**(json.loads(user_str)))


def decode_jwt_token(token: str) -> TokenPayload:
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    token_data = schemas.TokenPayload(**payload)
    return token_data

# def get_current_active_superuser(
#         current_user: UserModel = Depends(get_current_user),
# ) -> UserModel:
#     if not repository.user_repo.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user
