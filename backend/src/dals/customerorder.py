''' CustomerOrder Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.customerorder import CustomerOrder
from src.schemas.customerorder import CustomerOrderIn as data_in


class CustomerOrderDal():
    ''' load CustomerOrder dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, skip: int = 0, take: int = 20) -> List[CustomerOrder]:
        ''' load all customer orders '''
        query = await self.session\
            .execute(select(CustomerOrder)
                     .offset(skip).limit(take).order_by(CustomerOrder.stock_num))
        return query.scalars().fetchall()

    async def get_one(self, pid: int) -> CustomerOrder:
        ''' load one customer order by id '''
        query = await self.session.execute(select(CustomerOrder)
                                           .where(CustomerOrder.id == pid))
        return query.scalars().first()

    async def get_by_customer(self, pid: int) -> List[CustomerOrder]:
        ''' load orders by customer '''
        query = await self.session.execute(select(CustomerOrder)
                                           .where(CustomerOrder.customer_id == pid))
        return query.scalars().first()

    async def get_by_sales(self, pid: int) -> List[CustomerOrder]:
        ''' load orders by sales '''
        query = await self.session.execute(select(CustomerOrder)
                                           .where(CustomerOrder.sales_id == pid))
        return query.scalars().first()

    async def create(self, payload: data_in) -> CustomerOrder:
        ''' insert new CustomerOrder '''
        new_data = CustomerOrder(customer_id=payload.customer_id,
                                 sales_id=payload.sales_id,
                                 cash=payload.cash,
                                 created_at=payload.created_at)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> CustomerOrder:
        ''' update one customer order by id '''
        query = update(CustomerOrder)\
            .where(CustomerOrder.id == pid)\
            .values(customer_id=payload.customer_id,
                    sales_id=payload.sales_id,
                    cash=payload.cash,
                    created_at=payload.created_at)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete customer order by id '''
        query = delete(CustomerOrder).where(
            CustomerOrder.id == pid).returning(CustomerOrder.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
