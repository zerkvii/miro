from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import repository, models
from app.api import deps
from app.core import security
from app.schemas import OutMenu
from app.schemas.response import Response, STATUS
from app.schemas.user import InUser, OutUser

# content api
router = APIRouter()


@router.get('/week-data')
async def get_week_data(current_user: models.user = Depends(deps.get_current_user)):
    week_data = [
        {'x': '2022-07-01', 'y': 3},
        {'x': '2022-07-02', 'y': 5},
        {'x': '2022-07-03', 'y': 6},
        {'x': '2022-07-04', 'y': 10},
        {'x': '2022-07-05', 'y': -4},
        {'x': '2022-07-06', 'y': 30},
        {'x': '2022-07-07', 'y': 12},
    ]
    return Response(status=STATUS.SUCCESS, info='week_data access successful', data=week_data)


@router.get('/popular-list')
async def get_week_data(queryType: str, current_user: models.user = Depends(deps.get_current_user)):
    textList = [
        {
            'key': 1,
            'clickNumber': '346.3w+',
            'title': '经济日报：财政政策要精准提升…',
            'increases': 35,
        },
        {
            'key': 2,
            'clickNumber': '324.2w+',
            'title': '双12遇冷，消费者厌倦了电商平…',
            'increases': 22,
        },
        {
            'key': 3,
            'clickNumber': '318.9w+',
            'title': '致敬坚守战“疫”一线的社区工作…',
            'increases': 9,
        },
        {
            'key': 4,
            'clickNumber': '257.9w+',
            'title': '普高还是职高？家长们陷入选择…',
            'increases': 17,
        },
        {
            'key': 5,
            'clickNumber': '124.2w+',
            'title': '人民快评：没想到“浓眉大眼”的…',
            'increases': 37,
        },
    ]
    imageList = [
        {
            'key': 1,
            'clickNumber': '15.3w+',
            'title': '杨涛接替陆慷出任外交部美大司…',
            'increases': 15,
        },
        {
            'key': 2,
            'clickNumber': '12.2w+',
            'title': '图集：龙卷风袭击美国多州房屋…',
            'increases': 26,
        },
        {
            'key': 3,
            'clickNumber': '18.9w+',
            'title': '52岁大姐贴钱照顾自闭症儿童八…',
            'increases': 9,
        },
        {
            'key': 4,
            'clickNumber': '7.9w+',
            'title': '杭州一家三口公园宿营取暖中毒',
            'increases': 0,
        },
        {
            'key': 5,
            'clickNumber': '5.2w+',
            'title': '派出所副所长威胁市民？警方调…',
            'increases': 4,
        },
    ]
    videoList = [
        {
            'key': 1,
            'clickNumber': '367.6w+',
            'title': '这是今日10点的南京',
            'increases': 5,
        },
        {
            'key': 2,
            'clickNumber': '352.2w+',
            'title': '立陶宛不断挑衅致经济受损民众…',
            'increases': 17,
        },
        {
            'key': 3,
            'clickNumber': '348.9w+',
            'title': '韩国艺人刘在石确诊新冠',
            'increases': 30,
        },
        {
            'key': 4,
            'clickNumber': '346.3w+',
            'title': '关于北京冬奥会，文在寅表态',
            'increases': 12,
        },
        {
            'key': 5,
            'clickNumber': '271.2w+',
            'title': '95后现役军人荣立一等功',
            'increases': 2,
        },
    ]
    if queryType == 'image':
        data = imageList
    elif queryType == 'video':
        data = videoList
    else:
        data = textList
    return Response(status=STATUS.SUCCESS, info='week_data access successful', data=data)


@router.get('/category-sum')
async def get_category_sum(current_user: models.user = Depends(deps.get_current_user)):
    data = [
        {'name': '文本类', 'value': 102},
        {'name': '图片类', 'value': 144},
        {'name': '视频类', 'value': 122}
    ]
    return Response(status=STATUS.SUCCESS, info='category_sum access successful', data=data)
