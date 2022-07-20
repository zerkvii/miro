from fastapi import APIRouter, Depends

from app.api import deps
from app.models import UserModel
from app.schemas.response import Response, STATUS

# content api
from app.services.qiniu import get_bucket_info, get_prefix_list

router = APIRouter()


@router.get('')
async def get_music_list(current: int = 0, pageSize: int = 10,
                         current_user: UserModel = Depends(deps.get_current_user)):

    get_prefix_list()
    return Response(status=STATUS.SUCCESS, info='music list access successful')
