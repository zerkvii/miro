from app.db.db import AsyncIOMotorClient
from app.core.config import database_name, users_collection_name,user_menus_collection_name
from app.models.model import OutUser, MenuItem


async def get_user(conn: AsyncIOMotorClient, username: str) -> OutUser:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return OutUser(**row)


async def get_user_menus(conn: AsyncIOMotorClient, username: str) -> MenuItem:
    row = await conn[database_name][user_menus_collection_name].find_one({"username": username})
    print(row)
    if row:
        return MenuItem(**row)
# async def create_user(conn: AsyncIOMotorClient, user: User) -> User:
#     dbuser.change_password(user.password)
#
#     row = await conn[database_name][users_collection_name].insert_one(dbuser.dict())
#
#     dbuser.id = row.inserted_id
#     dbuser.created_at = ObjectId(dbuser.id ).generation_time
#     dbuser.updated_at = ObjectId(dbuser.id ).generation_time

# return dbuser
