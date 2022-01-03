''' Fackturer Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.fackturer import Fackturer
from src.schemas.fackturer import FackturerIn as data_in


class FackturerDal():
    ''' load Fackturer dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, skip: int = 0, take: int = 20) -> List[Fackturer]:
        ''' load all fackturers '''
        query = await self.session\
            .execute(select(Fackturer)
                     .offset(skip).limit(take).order_by(Fackturer.stock_num))
        return query.scalars().fetchall()

    async def get_one(self, pid: int) -> Fackturer:
        ''' load one fackturer by id '''
        query = await self.session.execute(select(Fackturer)
                                           .where(Fackturer.id == pid))
        return query.scalars().first()

    async def create(self, payload: data_in) -> Fackturer:
        ''' insert new Fackturer '''
        new_data = Fackturer(name=payload.name,
                             descriptions=payload.descriptions,
                             instructions=payload.instructions,
                             qty=payload.qty,
                             created_at=payload.created_at)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> Fackturer:
        ''' update one fackturer by id '''
        query = update(Fackturer)\
            .where(Fackturer.id == pid)\
            .values(name=payload.name,
                    descriptions=payload.descriptions,
                    instructions=payload.instructions,
                    qty=payload.qty,
                    created_at=payload.created_at)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete fackturer by id '''
        query = delete(Fackturer).where(
            Fackturer.id == pid).returning(Fackturer.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
