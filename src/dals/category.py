''' Category Dal '''
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload, Session
from src.models.category import Category
from src.schemas.category import CategoryIn as data_in


class CategoryDal():
    ''' load category dal '''

    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, skip: int = 0, take: int = 20) -> List[Category]:
        ''' load all categories '''
        query = await self.session.execute(select(Category)
                                           .offset(skip)
                                           .limit(take)
                                           .order_by(Category.name))
        return query.scalars().all()

    async def get_one(self, pid: int) -> Category:
        ''' load one category by id '''
        query = await self.session.execute(select(Category)
                                           .options(joinedload(Category.products))
                                           .where(Category.id == pid))
        return query.scalars().first()

    async def create(self, payload: data_in) -> Category:
        ''' insert new category '''
        new_data = Category(name=payload.name)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def modify(self, pid: int, payload: data_in) -> Category:
        ''' update one category by id '''
        query = update(Category).where(Category.id == pid)\
            .values(name=payload.name).returning(Category)
        query.execution_options(synchronize_session="fetch")
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return tup

    async def remove(self, pid: int) -> int:
        ''' delete category by id '''
        query = delete(Category).where(
            Category.id == pid).returning(Category.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
