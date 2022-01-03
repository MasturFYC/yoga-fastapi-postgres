''' Customer Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.customer import Customer
from src.schemas.customer import CustomerIn as data_in


class CustomerDal():
    ''' load Customer dal '''

    def __init__(self, session: Session):        
        self.session = session

    async def get_all(self, skip: int = 0, take: int = 20) -> List[Customer]:
        ''' load all Customers '''


        print('------------------------')
        query = await self.session.execute(select(Customer))
                     #.offset(skip).limit(take).order_by(Customer.name))

        print('------------------------')
        print('------------------------', query)


        return query.scalars().fetchall()

    async def get_one(self, pid: int) -> Customer:
        ''' load one Customer by id '''
        query = await self.session\
            .execute(select(Customer)
                     .where(Customer.id == pid))
        return query.scalars().first()

    async def create(self, payload: data_in) -> Customer:
        ''' insert new Customer '''
        new_supplier = Customer(name=payload.name,
                                street=payload.street,
                                city=payload.city,
                                phone=payload.phone,
                                cell=payload.cell,
                                zip=payload.zip,
                                email=payload.email)
        self.session.add(new_supplier)
        await self.session.flush()
        return new_supplier

    async def modify(self, pid: int, payload: data_in) -> Customer:
        ''' update one Customer by id '''
        query = update(Customer)\
            .where(Customer.id == pid)\
            .values(name=payload.name,
                    street=payload.street,
                    city=payload.city,
                    phone=payload.phone,
                    cell=payload.cell,
                    zip=payload.zip,
                    email=payload.email).returning(Customer)
        query.execution_options(synchronize_session="fetch")
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete Customer by id '''
        query = delete(Customer).where(
            Customer.id == pid).returning(Customer.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
