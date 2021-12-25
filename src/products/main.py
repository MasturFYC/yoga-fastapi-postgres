""" Product Router """

from typing import List
from fastapi import APIRouter, status
from sqlalchemy import select, update, insert, delete
from base import database
from product import Product
from schema import ProductIn, ProductOut

ROUTER = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"products": "Not found"}},
)


@ROUTER.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def read_products(skip: int = 0, take: int = 20):
    """ Get all products """
    query = select(Product).offset(skip).limit(take)
    return await database.fetch_all(query)


@ROUTER.get("/{prod_id}/", response_model=ProductIn, status_code=status.HTTP_200_OK)
async def read_product(prod_id: int):
    """ Get all product by id """
    query = select(Product).where(Product.id == prod_id)
    return await database.fetch_one(query)


@ROUTER.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_products(prod: ProductIn):
    """ Create product """
    query = insert(Product) \
        .values(name=prod.name, spec=prod.spec,
                base_unit=prod.base_unit, base_price=prod.base_price,
                base_weight=prod.base_weight, category_id=prod.category_id,
                first_stock=prod.first_stock, stock=prod.stock, is_active=True)
    last_record_id = await database.execute(query)
    return {**prod.dict(), "id": last_record_id}


@ROUTER.put("/{prod_id}/", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product(prod_id: int, prod: ProductIn):
    """ Update product by id """
    query = update(Product).where(Product.id == prod_id) \
        .values(name=prod.name, spec=prod.spec,
                base_unit=prod.base_unit, base_price=prod.base_price,
                base_weight=prod.base_weight, category_id=prod.category_id,
                first_stock=prod.first_stock, stock=prod.stock, is_active=prod.is_active)
    await database.execute(query)
    return {**prod.dict(), "id": prod_id}


@ROUTER.delete("/{prod_id}/", status_code=status.HTTP_200_OK)
async def delete_product(prod_id: int):
    """ Delete product by id """
    query = delete(Product).where(Product.id == prod_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(prod_id)}
