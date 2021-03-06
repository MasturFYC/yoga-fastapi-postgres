''' Unit Dal '''
from typing import List
from sqlalchemy import select, update, delete, Boolean, Integer
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.sql import text
from src.models.unit import Unit
from src.schemas.unit import UnitIn as data_in


class UnitDal():
    ''' load unit dal '''

    def __init__(self, session: Session):
        self.session = session

    async def unit_get_by_product(self, pid: int = 0) -> List[Unit]:
        ''' load all units '''
        query = await self.session\
            .execute(select(Unit)
                     .where(Unit.product_id == pid)
                     .order_by(Unit.content))
        return query.scalars().fetchall()

    async def unit_get_one(self, pid: int) -> Unit:
        ''' load one Unit by id '''
        query = await self.session.execute(select(Unit)
                                           .where(Unit.id == pid))
        return query.scalars().first()

    async def unit_insert(self, payload: data_in) -> Unit:
        ''' insert new Unit '''
        new_unit = Unit(product_id=payload.product_id,
                        name=payload.name,
                        barcode=payload.barcode,
                        content=payload.content,
                        buy_price=payload.buy_price,
                        margin=payload.margin,
                        price=payload.price,
                        is_default=payload.is_default)
        self.session.add(new_unit)
        await self.session.flush()
        return new_unit

    async def unit_update(self, pid: int, payload: data_in) -> Unit:
        ''' update one Unit by id '''

        if(payload.is_default == True):
            sql_file1 = open('src/dals/unit_clear_default.sql', 'r')
            # sql_file2 = open('src/dals/update_unit_default.sql', 'r')

            stmt = text(sql_file1.read())
            stmt = stmt.bindparams(bindparam('val',
                                             value=False,
                                             type_=Boolean),
                                   bindparam('id',
                                             value=pid,
                                             type_=Integer),
                                   bindparam('product_id',
                                             value=payload.product_id,
                                             type_=Integer)
                                   )
            await self.session.execute(stmt)

            sql_file1.close()

            # stmt = text(sql_file2.read())
            # stmt = stmt.bindparams(bindparam('val',
            #                                   value=payload.is_default,
            #                                   type_=Boolean),
            #                         bindparam('id',
            #                                   value=pid,
            #                                   type_=Integer),
            #                         )
            # await self.session.execute(stmt)

            # sql_file2.close()

        query = update(Unit).where(Unit.id == pid)\
            .values(product_id=payload.product_id,
                    name=payload.name,
                    barcode=payload.barcode,
                    content=payload.content,
                    buy_price=payload.buy_price,
                    margin=payload.margin,
                    price=payload.price,
                    is_default=payload.is_default).returning(Unit)
        query.execution_options(synchronize_session="fetch")
        res = await self.session.execute(query)
        tup = res.fetchone()

        await self.session.commit()
        return tup

    async def unit_delete(self, pid: int) -> int:
        ''' delete Unit by id '''
        query = delete(Unit).where(
            Unit.id == pid).returning(Unit.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
