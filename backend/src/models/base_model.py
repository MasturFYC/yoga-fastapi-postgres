""" base model """

import urllib
import databases
from env_loader import load_env
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

env = load_env(dir_path='./', auto_parse=True)

HOST_SERVER = env.get('HOST_SERVER')
DB_SERVER_PORT = int(str(env.get('DB_PORT')))
DB_NAME = env.get('DB_NAME')
DB_USER_NAME = env.get('DB_USERNAME')
DB_PASSWORD = env.get('DB_PASSWORD')
SSL_MODEL = env.get('SSL_MODE')

DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}:{}/{}?prepared_statement_cache_size=500'.format(
    DB_USER_NAME, DB_PASSWORD, HOST_SERVER, DB_SERVER_PORT, DB_NAME)

engine = create_async_engine(
    DATABASE_URL, pool_size=3, max_overflow=0, echo=True,)

declare_base = declarative_base()

db_session = sessionmaker(engine, class_=AsyncSession,
                          expire_on_commit=False, autocommit=False)
database = databases.Database(DATABASE_URL)


class CamelModel(BaseModel):
    ''' base model but non camel '''
    class Config:
        ''' doc string '''
        allow_population_by_field_name = True
        orm_mode = True