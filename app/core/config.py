import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_V1_STR = "/api"

JWT_TOKEN_PREFIX = "Bearer"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "MIRO")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

# deploying without docker-compose
MONGODB_URL = os.getenv("MONGODB_URL",
                        "mongodb://zerkvii:!Whu123456@121.37.147.23:27017")
# if not MONGODB_URL:
#     MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
#     MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
#     MONGO_USER = os.getenv("MONGO_USER", "admin")
#     MONGO_PASS = os.getenv("MONGO_PASSWORD", "markqiu")
#     MONGO_DB = os.getenv("MONGO_DB", "fastapi")
#
#     MONGODB_URL = DatabaseURL(
#         f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
#     )
# else:
#     MONGODB_URL = DatabaseURL(MONGODB_URL)

database_name = os.getenv('MONGO_DB', 'miro')
article_collection_name = "articles"
favorites_collection_name = "favorites"
tags_collection_name = "tags"
users_collection_name = "users"
user_menus_collection_name = "user_menus"
comments_collection_name = "commentaries"