# from pymongo import MongoClient

# client = MongoClient("mongodb+srv://zerkvii:zerkvii@cluster0.u65gi.mongodb.net/zee?retryWrites=true&w=majority")

#
# def get_db(name: str = 'fs'):
#     db = client.get_database(name)
#     return db
from motor.motor_asyncio import AsyncIOMotorClient

import logging

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    logging.info("连接数据库中...")
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("连接数据库成功！")


async def close_mongo_connection():
    logging.info("关闭数据库连接...")
    db.client.close()
    logging.info("数据库连接关闭！")
