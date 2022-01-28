import asyncio
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm.session import sessionmaker
from db import engine, declare_base, db_session


sp_stock_before_insert = """
CREATE OR REPLACE FUNCTION sp_stocks_before_insert()
 RETURNS trigger
 LANGUAGE plpgsql
AS $$

begin

    NEW.remain_payment = NEW.total - (NEW.cash + NEW.payment);

    RETURN NEW;

end;
$$;
"""

DROP1 = """
DROP TRIGGER IF EXISTS stocks_before_insert ON stocks;
"""

trigger_stock_before_insert = """
CREATE TRIGGER stocks_before_insert
BEFORE INSERT OR UPDATE ON stocks
FOR EACH ROW EXECUTE PROCEDURE sp_stocks_before_insert();
"""

async def async_main(AsyncronEngine: AsyncEngine, AsyncronSession: sessionmaker):

    async with AsyncronEngine.begin() as conn:
        await conn.execute(DDL(sp_stock_before_insert))
        await conn.execute(DDL(DROP1))
        await conn.execute(DDL(trigger_stock_before_insert))

    await AsyncronEngine.dispose()

asyncio.run(async_main(engine, db_session))
