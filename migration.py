import asyncio

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm.session import sessionmaker

from base import engine, Base, Session
from category import Category
from product import Product
from unit import Unit


async def async_main(AsyncronEngine: AsyncEngine, AsyncronSession: sessionmaker):

    async with AsyncronEngine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncronSession() as session:

        async with session.begin():
            await conn.run_sync(Category.__table__.create(bind=engine, checkfirst=True))
            await AsyncronSession.commit()
            await conn.run_sync(Product.__table__.create(bind=engine, checkfirst=True))
            await AsyncronSession.commit()
            await conn.run_sync(Unit.__table__.create(bind=engine, checkfirst=True))
            await AsyncronSession.commit()

    await AsyncronEngine.dispose()

asyncio.run(async_main(engine, Session))
