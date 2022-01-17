""" base model """

import calendar
from datetime import datetime, timezone
import urllib
import databases
from env_loader import load_env
import pytz
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

env = load_env(dir_path='./', auto_parse=True)

DB_HOST = env.get('DB_HOST')
DB_HOST_PORT = int(str(env.get('DB_HOST_PORT')))
DB_NAME = env.get('DB_NAME')
DB_USER_NAME = env.get('DB_USERNAME')
DB_PASSWORD = env.get('DB_PASSWORD')
SSL_MODEL = env.get('SSL_MODE')

DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}:{}/{}?prepared_statement_cache_size=500'.format(
    DB_USER_NAME, DB_PASSWORD, DB_HOST, DB_HOST_PORT, DB_NAME)

engine = create_async_engine(
    DATABASE_URL, pool_size=3, max_overflow=0, echo=True,)

declare_base = declarative_base()

db_session = sessionmaker(engine, class_=AsyncSession,
                          expire_on_commit=False, autocommit=False)
database = databases.Database(DATABASE_URL)


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    # dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return dt.astimezone(pytz.timezone('Asia/Jakarta')).strftime('%Y-%m-%dT%H:%M:%SZ')

class CamelModel(BaseModel):
    ''' base model but non camel '''
    class Config:
        ''' doc string '''
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {
            datetime: lambda v: convert_datetime_to_iso_8601_with_z_suffix(v)
        }
