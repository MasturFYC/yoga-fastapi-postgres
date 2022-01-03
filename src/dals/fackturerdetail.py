''' FackturerDetail Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.models.fackturerdetail import FackturerDetail
from src.schemas.fackturerdetail import FackturerDetailIn as data_in


class FackturerDetailDal():
    ''' load FackturerDetail dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_one(self, pid: int) -> FackturerDetail:
        ''' load one fackturer detail by id '''
        query = await self.session.execute(select(FackturerDetail)
                                           .where(FackturerDetail.id == pid))
        return query.scalars().first()

    async def get_by_fackturer(self, pid: int = 0) -> List[FackturerDetail]:
        ''' load all fackturer details '''
        query = await self.session\
            .execute(select(FackturerDetail)
                     .where(FackturerDetail.fackturer_id == pid)
                     .order_by(FackturerDetail.id))
        return query.scalars().fetchall()

    async def create(self, payload: data_in) -> FackturerDetail:
        ''' insert new fackturer detail '''
        new_data = FackturerDetail(fackturer_id=payload.fackturer_id,
                                   unit_id=payload.unit_id,
                                   qty=payload.qty,
                                   content=payload.content,
                                   unit_name=payload.unit_name,
                                   price=payload.price)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> FackturerDetail:
        ''' update one fackturer detail by id '''
        query = update(FackturerDetail).where(FackturerDetail.id == pid)\
            .values(fackturer_id=payload.fackturer_id,
                    unit_id=payload.unit_id,
                    qty=payload.qty,
                    content=payload.content,
                    unit_name=payload.unit_name,
                    price=payload.price)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete fackturer detail by id '''
        query = delete(FackturerDetail).where(
            FackturerDetail.id == pid).returning(FackturerDetail.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
