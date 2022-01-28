import asyncio
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm.session import sessionmaker
from db import engine, declare_base, db_session


sp_stock_detail_before_insert = """
CREATE OR REPLACE FUNCTION sp_stock_details_before_insert()
 RETURNS trigger
 LANGUAGE plpgsql
AS $$

begin

    NEW.real_qty = NEW.qty * NEW.content;
    NEW.subtotal = NEW.qty * (NEW.price - NEW.discount);

    RETURN NEW;

end;
$$;
"""
sp_stock_detail_after_insert = """
CREATE OR REPLACE FUNCTION sp_stock_details_after_insert()
 RETURNS trigger
 LANGUAGE plpgsql
AS $$

begin

    UPDATE stocks SET
    total = total + NEW.subtotal
    WHERE id = NEW.stock_id;

    UPDATE products SET
    stock = stock - NEW.real_qty
    WHERE id = NEW.product_id;

    RETURN NEW;

end;
$$;
"""

sp_stock_detail_after_update = """
CREATE OR REPLACE FUNCTION sp_stock_details_after_update()
 RETURNS trigger
 LANGUAGE plpgsql
AS $$

begin

    UPDATE stocks SET
    total = total - OLD.subtotal  + NEW.subtotal
    WHERE id = NEW.stock_id;

    if OLD.product_id = NEW.product_id then

        UPDATE products SET
        stock = stock + OLD.real_qty - NEW.real_qty
        WHERE id = NEW.product_id;

    else

        UPDATE products SET
        stock = stock + OLD.real_qty
        WHERE id = OLD.product_id;

        UPDATE products SET
        stock = stock - NEW.real_qty
        WHERE id = NEW.product_id;

    end if;

    RETURN NEW;

end;
$$;
"""

sp_stock_detail_after_delete = """
CREATE OR REPLACE FUNCTION sp_stock_details_after_delete()
 RETURNS trigger
 LANGUAGE plpgsql
AS $$

begin

    UPDATE stocks SET
    total = total - OLD.subtotal
    WHERE id = OLD.stock_id;

    UPDATE products SET
    stock = stock + OLD.real_qty
    WHERE id = OLD.product_id;

    RETURN OLD;

end;
$$;
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
trigger_stock_detail_after_update = """
CREATE TRIGGER stock_details_after_update
AFTER UPDATE ON stock_details
FOR EACH ROW EXECUTE PROCEDURE sp_stock_details_after_update();
"""
trigger_stock_detail_after_delete = """
CREATE TRIGGER stock_details_after_delete
AFTER DELETE ON stock_details
FOR EACH ROW EXECUTE PROCEDURE sp_stock_details_after_delete();
"""

async def async_main(AsyncronEngine: AsyncEngine, AsyncronSession: sessionmaker):

    async with AsyncronEngine.begin() as conn:
        # await conn.run_sync(declare_base.metadata.drop_all)
        # await conn.run_sync(declare_base.metadata.create_all)
        await conn.execute(DDL(sp_stock_detail_before_insert))
        await conn.execute(DDL(sp_stock_detail_after_insert))
        await conn.execute(DDL(sp_stock_detail_after_update))
        await conn.execute(DDL(sp_stock_detail_after_delete))
        await conn.execute(DDL("DROP TRIGGER IF EXISTS stock_details_before_insert ON stock_details;"))
        await conn.execute(DDL("DROP TRIGGER IF EXISTS stock_details_after_delete ON stock_details;"))
        await conn.execute(DDL("DROP TRIGGER IF EXISTS stock_details_after_update ON stock_details;"))
        await conn.execute(DDL("DROP TRIGGER IF EXISTS stock_details_after_insert ON stock_details;"))
        await conn.execute(DDL(trigger_stock_detail_before_insert))
        await conn.execute(DDL(trigger_stock_detail_after_insert))
        await conn.execute(DDL(trigger_stock_detail_after_update))
        await conn.execute(DDL(trigger_stock_detail_after_delete))

    await AsyncronEngine.dispose()

asyncio.run(async_main(engine, db_session))
