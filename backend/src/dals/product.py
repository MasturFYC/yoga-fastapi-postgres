''' Product Dal '''
from typing import List
from sqlalchemy import and_, or_, select, update, delete, DECIMAL, Integer
from sqlalchemy.orm import joinedload, Session, selectinload,  load_only
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.sql import text
from sqlalchemy import func
from src.models.product import Product
from src.schemas.product import ProductIn as data_in


class ProductDal():
    ''' load product dal '''

    def __init__(self, session: Session):
        self.session = session

    async def product_get_all(self, skip: int = 0, take: int = 20) -> List[Product]:
        ''' load all products '''
        query = await self.session\
            .execute(select(Product)
                     .offset(skip).limit(take)
                     .order_by(Product.name))

        return query.scalars().fetchall()

    async def get_by_category(self, category_id: int = 0) -> List[Product]:
        ''' load all products '''
        query = await self.session\
            .execute(select(Product)
                     .where(or_(Product.category_id == category_id, category_id == 0))
                     .order_by(Product.name))

        return query.scalars().fetchall()

    async def search_name(self, name: str) -> List[Product]:
        ''' search products by name '''
        query = await self.session.execute(select(Product)
                                           .where(func.lower(Product.name).contains(name.lower()))
                                           .order_by(Product.name))
        print(str(query))
        return query.scalars().fetchall()

    async def get_with_units(self):
        ''' load all products '''
        query = await self.session\
            .execute(select(Product)
                     .options(load_only(Product.id,
                                        Product.name,
                                        Product.spec,
                                        Product.stock,
                                        Product.is_active,
                                        Product.is_sale))
                     .options(selectinload(Product.units))
                     .where(and_(Product.is_active == True, Product.category_id > 1))
                     .order_by(Product.name))
        rs = query.scalars().fetchall()
        await self.session.commit()

        return rs

    async def product_get_one(self, pid: int) -> Product:
        ''' load one Product by id '''
        query = await self.session.execute(select(Product)
                                           .options(joinedload(Product.units))
                                           .where(Product.id == pid))
        return query.scalars().first()

    async def product_insert(self, payload: data_in) -> Product:
        ''' insert new Product '''
        new_product = Product(category_id=payload.category_id,
                              name=payload.name,
                              spec=payload.spec,
                              base_unit=payload.base_unit,
                              base_price=payload.base_price,
                              base_weight=payload.base_weight,
                              first_stock=payload.first_stock,
                              is_active=payload.is_active,
                              is_sale=payload.is_sale,
                              )
        self.session.add(new_product)
        await self.session.flush()
        return new_product

    async def product_update(self, pid: int, payload: data_in) -> Product:
        ''' update one Product by id '''
        sql_file = open('src/dals/update_unit_price.sql', 'r')

        query = update(Product).where(Product.id == pid)\
            .values(category_id=payload.category_id,
                    name=payload.name,
                    spec=payload.spec,
                    base_unit=payload.base_unit,
                    base_price=payload.base_price,
                    base_weight=payload.base_weight,
                    first_stock=payload.first_stock,
                    is_active=payload.is_active,
                    is_sale=payload.is_sale,).returning(Product)
        query.execution_options(synchronize_session="fetch")
        res = await self.session.execute(query)

        stmt = text(sql_file.read())
        stmt = stmt.bindparams(bindparam('base_price',
                                         value=payload.base_price,
                                         type_=DECIMAL(12, 2)),
                               bindparam('id',
                                         value=pid,
                                         type_=Integer))
        stmt.execution_options(autocommit=False)
        await self.session.execute(stmt)

        tup = res.fetchone()
        await self.session.commit()

        # self.session.close()
        sql_file.close()

        return tup

    async def product_delete(self, pid: int) -> int:
        ''' delete Product by id '''
        query = delete(Product).where(
            Product.id == pid).returning(Product.id)
        res = await self.session.execute(query)
        tup = res.fetchone()
        await self.session.commit()
        return {'id': tup.id}
