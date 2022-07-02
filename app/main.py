from fastapi import FastAPI, Depends
from typing import Optional
# from app.depends import get_query_token, get_token_header
from app.db.db import connect_to_mongo, close_mongo_connection
from app.routes import user_rt
from app.internal import admin_rt
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI(
    # dependencies=[Depends(get_query_token)]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(user_rt.router, prefix='/api')
# app.include_router(
#     admin_rt.router,
#     prefix='/admins',
#     tags=['admins'],
#     # dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}}, )


@app.get('/')
async def root():
    """sample index

    Returns:
        _type_: _description_
    """
    return {
        'message': f'welcome to this app'
    }


@app.post("/auth")
async def page_login(name: str, password: str, remember: Optional[bool]):
    print(name, password, remember)
    return {"status_code": 200, 'data': 'eyjb'}
