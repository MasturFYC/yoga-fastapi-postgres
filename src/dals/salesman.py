''' Salesman Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.salesman import Salesman
from src.schemas.salesman import SalesmanIn as data_in


class SalesmanDal():
    ''' load salesman dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, skip: int = 0, take: int = 20) -> List[Salesman]:
        ''' load all salesmans '''
        query = await self.session\
            .execute(select(Salesman)
                     .offset(skip).limit(take)
                     .order_by(Salesman.name))
        return query.scalars().fetchall()

    async def get_one(self, pid: int) -> Salesman:
        ''' load one Salesman by id '''
        query = await self.session\
            .execute(select(Salesman)
                     .where(Salesman.id == pid))
        return query.scalars().first()

    async def create(self, payload: data_in) -> Salesman:
        ''' insert new salesman '''
        new_data = Salesman(name=payload.name,
                            street=payload.street,
                            city=payload.city,
                            phone=payload.phone,
                            cell=payload.cell,
                            zip=payload.zip,
                            email=payload.email)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> Salesman:
        ''' update one salesman by id '''
        query = update(Salesman)\
            .where(Salesman.id == pid)\
            .values(name=payload.name,
                    street=payload.street,
                    city=payload.city,
                    phone=payload.phone,
                    cell=payload.cell,
                    zip=payload.zip,
                    email=payload.email).returning(Salesman)
        query.execution_options(synchronize_session="fetch")
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete salesman by id '''
        query = delete(Salesman).where(
            Salesman.id == pid).returning(Salesman.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
