''' OrderDetail Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.orderdetail import OrderDetail
from src.schemas.orderdetail import OrderDetailIn as data_in


class OrderDetailDal():
    ''' load OrderDetail dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_one(self, pid: int) -> OrderDetail:
        ''' load one order detail by id '''
        query = await self.session.execute(select(OrderDetail)
                                           .where(OrderDetail.id == pid))
        return query.scalars().first()

    async def get_by_order(self, pid: int = 0) -> List[OrderDetail]:
        ''' load all order details '''
        query = await self.session\
            .execute(select(OrderDetail)
                     .where(OrderDetail.order_id == pid)
                     .order_by(OrderDetail.id))
        return query.scalars().fetchall()

    async def create(self, payload: data_in) -> OrderDetail:
        ''' insert new order detail '''
        new_data = OrderDetail(order_id=payload.order_id,
                               unit_id=payload.unit_id,
                               qty=payload.qty,
                               content=payload.content,
                               unit_name=payload.unit_name,
                               price=payload.price,
                               buy_price=payload.buy_price,
                               discount=payload.discount)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> OrderDetail:
        ''' update one order detail by id '''
        query = update(OrderDetail).where(OrderDetail.id == pid)\
            .values(order_id=payload.order_id,
                    unit_id=payload.unit_id,
                    qty=payload.qty,
                    content=payload.content,
                    unit_name=payload.unit_name,
                    price=payload.price,
                    buy_price=payload.buy_price,
                    discount=payload.discount)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete order detail by id '''
        query = delete(OrderDetail).where(
            OrderDetail.id == pid).returning(OrderDetail.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
