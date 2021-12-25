""" Unit Router """

from typing import List
from fastapi import APIRouter, status
from sqlalchemy import select, update, insert, delete
from base import database
from unit import Unit
from schema import UnitIn, UnitOut

ROUTER = APIRouter(
    prefix="/units",
    tags=["units"],
    responses={404: {"units": "Not found"}},
)


@ROUTER.get("/", response_model=List[UnitOut], status_code=status.HTTP_200_OK)
async def read_units(skip: int = 0, take: int = 20):
    """ Get all units """
    query = select(Unit).offset(skip).limit(take)
    return await database.fetch_all(query)


@ROUTER.get("/{unit_id}/", response_model=UnitIn, status_code=status.HTTP_200_OK)
async def read_unit(unit_id: int):
    """ Get all unit by id """
    query = select(Unit).where(Unit.id == unit_id)
    return await database.fetch_one(query)


@ROUTER.post("/", response_model=UnitOut, status_code=status.HTTP_201_CREATED)
async def create_units(unit: UnitIn):
    """ Create unit """
    query = insert(Unit) \
        .values(product_id=unit.product_id, name=unit.name, content=unit.content,
                buy_price=unit.buy_price, margin=unit.margin, price=unit.price,
                is_default=False)
    last_record_id = await database.execute(query)
    return {**unit.dict(), "id": last_record_id}


@ROUTER.put("/{unit_id}/", response_model=UnitOut, status_code=status.HTTP_200_OK)
async def update_unit(unit_id: int, unit: UnitIn):
    """ Update unit by id """
    query = update(Unit).where(Unit.id == unit_id) \
        .values(product_id=unit.product_id, name=unit.name, content=unit.content,
                buy_price=unit.buy_price, margin=unit.margin, price=unit.price,
                is_default=unit.is_default)
    await database.execute(query)
    return {**unit.dict(), "id": unit_id}


@ROUTER.delete("/{unit_id}/", status_code=status.HTTP_200_OK)
async def delete_unit(unit_id: int):
    """ Delete unit by id """
    query = delete(Unit).where(Unit.id == unit_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(unit_id)}
