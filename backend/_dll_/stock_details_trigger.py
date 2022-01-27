import asyncio
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm.session import sessionmaker
from db import engine, declare_base, db_session


sp_stock_detail_before_insert = """
CREATE OR REPLACE FUNCTION sp_stock_details_before_insert()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

begin

    NEW.real_qty = NEW.qty * NEW.content;
    NEW.subtotal = NEW.qty * (NEW.price - NEW.discount);

    RETURN NEW;

end;
$function$;
"""
sp_stock_detail_after_insert = """
CREATE OR REPLACE FUNCTION sp_stock_details_after_insert()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

begin

    UPDATE stocks SET
    total = total + NEW.subtotal
    WHERE id = NEW.stock_id;

    UPDATE products SET
    stock = stock + NEW.real_qty
    WHERE id = NEW.product_id;

    RETURN NEW;

end;
$function$;
"""

trigger_stock_detail_before_insert = """
CREATE TRIGGER stock_details_before_insert
BEFORE INSERT OR UPDATE ON stock_details
FOR EACH ROW EXECUTE PROCEDURE sp_stock_details_before_insert();
"""
trigger_stock_detail_after_insert = """
CREATE TRIGGER stock_details_after_insert
AFTER INSERT ON stock_details
FOR EACH ROW EXECUTE PROCEDURE sp_stock_details_after_insert();
"""

async def async_main(AsyncronEngine: AsyncEngine, AsyncronSession: sessionmaker):

    async with AsyncronEngine.begin() as conn:
        # await conn.run_sync(declare_base.metadata.drop_all)
        # await conn.run_sync(declare_base.metadata.create_all)
        await conn.execute(DDL(sp_stock_detail_before_insert))
        await conn.execute(DDL(sp_stock_detail_after_insert))
        await conn.execute(DDL(trigger_stock_detail_before_insert))
        await conn.execute(DDL(trigger_stock_detail_after_insert))

    await AsyncronEngine.dispose()

asyncio.run(async_main(engine, db_session))
