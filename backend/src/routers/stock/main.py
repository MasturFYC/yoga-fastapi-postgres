""" Stock Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.schemas.stock import StockIn as data_in, StockOut as data_out
from src.dals.stock import StockDal as cur_dal


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/api/stocks",
    tags=["stocks"],
    responses={404: {"Stock": "Not found"}},
)


@ROUTER.get("/", response_model=List[data_out], status_code=status.HTTP_200_OK)
async def read_stocks(skip: int = 0, take: int = 20, dal: cur_dal = Depends(get_current_dal)):
    """ Get all stocks """
    res = await dal.get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Stock is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def read_stock(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get stock by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Stock not found")

    return res.__dict__


@ROUTER.get("/suppler/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def get_by_supplier(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get stock by supplier """
    res = await dal.get_by_supplier(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Stock not found")

    return [row.__dict__ for row in res]


@ROUTER.post("/", response_model=data_out, status_code=status.HTTP_201_CREATED)
async def create_stock(payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Create stock """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Stock name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def update_stock(pid: int, payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Update stock by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Stock name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_stock(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete stock by id """
    return await dal.remove(pid)
