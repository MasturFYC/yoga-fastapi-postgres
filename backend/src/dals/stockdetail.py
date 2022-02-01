''' stock detail Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.stockdetail import StockDetail
from src.schemas.stockdetail import StockDetailIn as data_in


class StockDetailDal():
    ''' load stock detail dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_one(self, pid: int) -> StockDetail:
        ''' load one stock detail by id '''
        query = await self.session.execute(select(StockDetail)
                                           .where(StockDetail.id == pid))
        return query.scalars().first()

    async def get_by_stock(self, pid: int = 0) -> List[StockDetail]:
        ''' load all stock detail '''
        query = await self.session\
            .execute(select(StockDetail)
                     .where(StockDetail.stock_id == pid)
                     .order_by(StockDetail.id))
        return query.scalars().fetchall()

    async def create(self, payload: data_in) -> StockDetail:
        ''' insert new stock detail '''

        new_data = StockDetail(qty=payload.qty,
                               content=payload.content,
                               unit_name=payload.unit_name,
                               price=payload.price,
                               discount=payload.discount,
                               stock_id=payload.stock_id,
                               product_id=payload.product_id,
                               unit_id=payload.unit_id)
        self.session.add(new_data)
        await self.session.flush()
        new_data.subtotal = payload.qty * (payload.price - payload.discount)
        new_data.real_qty = payload.qty * payload.content
        return new_data

    async def modify(self, pid: int, payload: data_in) -> StockDetail:
        ''' update one stock detail by id '''
        query = update(StockDetail).where(StockDetail.id == pid)\
            .values(qty=payload.qty,
                    content=payload.content,
                    unit_name=payload.unit_name,
                    price=payload.price,
                    discount=payload.discount,
                    stock_id=payload.stock_id,
                    product_id=payload.product_id,
                    unit_id=payload.unit_id)\
            .returning(StockDetail)

        query.execution_options(synchronize_session="fetch")
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete stock detail by id '''
        query = delete(StockDetail).where(
            StockDetail.id == pid).returning(StockDetail.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
