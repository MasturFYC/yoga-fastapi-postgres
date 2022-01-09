""" Customer Order Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.schemas.customerorder import CustomerOrderIn as data_in, CustomerOrderOut as data_out
from src.dals.customerorder import CustomerOrderDal as cur_dal


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/api/orders",
    tags=["orders"],
    responses={404: {"Order": "Not found"}},
)


@ROUTER.get("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def read_order(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get order by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Order not found")

    return res.__dict__


@ROUTER.get("/", response_model=List[data_out], status_code=status.HTTP_200_OK)
async def read_orders(skip: int = 0, take: int = 20, dal: cur_dal = Depends(get_current_dal)):
    """ Get all orders """
    res = await dal.get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Order is empty")
    return [row.__dict__ for row in res]

@ROUTER.get("/customer/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def get_by_customer(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get order by customer """
    res = await dal.get_by_customer(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Order not found")

    return [row.__dict__ for row in res]


@ROUTER.get("/sales/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def get_by_sales(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get order by customer """
    res = await dal.get_by_sales(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Order not found")

    return [row.__dict__ for row in res]

@ROUTER.post("/", response_model=data_out, status_code=status.HTTP_201_CREATED)
async def create_order(payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Create order """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Order name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def update_order(pid: int, payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Update order by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Order name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_order(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete order by id """
    return await dal.remove(pid)
