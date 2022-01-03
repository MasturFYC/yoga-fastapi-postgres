''' Stock Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.stock import Stock
from src.schemas.stock import StockIn as data_in


class StockDal():
    ''' load Stock dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, skip: int = 0, take: int = 20) -> List[Stock]:
        ''' load all stocks '''
        query = await self.session\
            .execute(select(Stock)
                     .offset(skip).limit(take).order_by(Stock.stock_num))
        return query.scalars().fetchall()

    async def get_by_supplier(self, pid: int = 0) -> List[Stock]:
        ''' load all stocks by supplier '''
        query = await self.session\
            .execute(select(Stock)
                     .where(Stock.supplier_id == pid)
                     .order_by(Stock.id))
        return query.scalars().fetchall()


    async def get_one(self, pid: int) -> Stock:
        ''' load one stock by id '''
        query = await self.session.execute(select(Stock)
                                           .where(Stock.id == pid))
        return query.scalars().first()

    async def create(self, payload: data_in) -> Stock:
        ''' insert new Stock '''
        new_data = Stock(supplier_id=payload.supplier_id,
                         stock_num=payload.stock_num,
                         cash=payload.cash,
                         created_at=payload.created_at)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> Stock:
        ''' update one stock by id '''
        query = update(Stock).where(Stock.id == pid)\
            .values(supplier_id=payload.supplier_id,
                    stock_num=payload.stock_num,
                    cash=payload.cash,
                    created_at=payload.created_at)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete stock by id '''
        query = delete(Stock).where(
            Stock.id == pid).returning(Stock.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
