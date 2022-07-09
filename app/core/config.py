import json
import secrets
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator, AnyUrl, BaseModel
from pathlib import Path

from pydantic.env_settings import SettingsSourceCallable


def json_config_settings_source(json_settings: BaseSettings) -> Dict[str, Any]:
    encoding = json_settings.__config__.env_file_encoding
    ret = json.loads(Path('config.json').read_text(encoding=encoding))
    return ret


# class LogConfig(BaseModel):
#     LOGGER_NAME: str = 'miro'
#     LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
#     LOG_LEVEL: str = "DEBUG"
#
#     # Logging config
#     version: int = 1
#     disable_existing_loggers: bool = False
#     formatters: Dict[str, Any] = {
#         "default": {
#             # "()": "uvicorn.logging.DefaultFormatter",
#             "fmt": LOG_FORMAT,
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     }
#     handlers: Dict[str, Any] = {
#         "default": {
#             # "formatter": "default",
#             "class": "logging.FileHandler",
#             'filename': 'logs/miro.log',
#             # 'mode': 'a',
#             # 'maxBytes': 10 * 1024 * 1024,
#             # 'backupCount': 10,
#         }
#     }
#     loggers: Dict[str, Any] = {
#         'miro': {"handlers": ["default"], "level": LOG_LEVEL},
#     }
#

class Settings(BaseSettings):
    class Config:
        env_file_encoding = 'utf-8'
        case_sensitive = False

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings) -> Tuple[
            SettingsSourceCallable, ...]:
            return init_settings, json_config_settings_source, env_settings, file_secret_settings

    API_V1_STR: str
    WS_API: str
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(days=8)
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '['http://localhost', 'http://localhost:4200', 'http://localhost:3000', \
    # 'http://localhost:8080', 'http://local.dockertoolbox.tiangolo.com']'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    # SENTRY_DSN: Optional[HttpUrl] = None
    #
    # @validator('SENTRY_DSN', pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[AnyUrl] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AnyUrl.build(
            scheme='mysql+pymysql',
            user=values.get('MYSQL_USER'),
            password=values.get('MYSQL_PASSWORD'),
            host=values.get('MYSQL_SERVER'),
            path=f'/{values.get("MYSQL_DB") or ""}',
        )

    REDIS_URL: Optional[AnyUrl] = None

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_NAME: str
    ALLOW_SQL_ECHO: bool = False

    # LOG_CONF: LogConfig = LogConfig()
    # USERS_OPEN_REGISTRATION: bool = False
    LOG_FILE: str = None
    LOG_FILE_FORMAT: str = "<green>{time}</green> - {level} - {message}"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_COMPRESSION: str = 'tar.gz'
    LOG_FILE_ROTATION = '100 MB'
    # ACTIVE_USERS: str = 'active_users'
    ACTIVE_USERS_INFO: str = 'active_users_info'
    CHAT_HISTORY_KEY: str = 'chat_history'


settings = Settings()
