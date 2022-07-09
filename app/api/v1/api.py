from fastapi import APIRouter

from app.api.v1.endpoints import users, contents

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
ws_api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
