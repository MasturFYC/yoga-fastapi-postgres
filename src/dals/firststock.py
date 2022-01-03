''' First Stock Dal '''

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.firststock import FirstStock as fs
from src.schemas.firststock import FirstStockIn as fs_in


class FirstStockDal():
    ''' load First Stock dal '''

    def __init__(self, session: Session):
        self.session = session

    async def firststock_get_one(self, pid: int) -> fs:
        ''' load one first stock by id '''
        query = await self.session.execute(select(fs)
                                           .where(fs.product_id == pid))
        return query.scalars().first()

    async def firststock_insert(self, payload: fs_in) -> fs:
        ''' insert new fs '''
        new_data = fs(product_id=payload.product_id,
                      unit_id=payload.unit_id,
                      qty=payload.qty,
                      unit_name=payload.unit_name,
                      content=payload.content)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def firststock_update(self, pid: int, payload: fs_in) -> fs:
        ''' update one first stock by id '''
        query = update(fs).where(fs.product_id == pid)\
            .values(product_id=payload.product_id,
                    unit_id=payload.unit_id,
                    qty=payload.qty,
                    unit_name=payload.unit_name,
                    content=payload.content)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def firststock_delete(self, pid: int) -> int:
        ''' delete first stock by id '''
        query = delete(fs).where(
            fs.product_id == pid).returning(fs.product_id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'product_id': tup.product_id}
