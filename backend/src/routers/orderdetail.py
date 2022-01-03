""" OrderDetail Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.dals.orderdetail import OrderDetailDal as cur_dal
from src.schemas.orderdetail import OrderDetailIn as data_in,\
    OrderDetailOut as data_out


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/orderdetails",
    tags=["orderdetails"],
    responses={404: {"Order Detail": "Not found"}},
)


@ROUTER.get("/order/{pid}",
            response_model=List[data_out],
            status_code=status.HTTP_200_OK)
async def read_orderdetails(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get order details by order """
    res = await dal.get_by_order(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Order details is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def read_orderdetail(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get order detail by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Order details is empty")
    return res.__dict__


@ROUTER.post("/", response_model=data_out, status_code=status.HTTP_201_CREATED)
async def create_orderdetail(payload: data_in,
                             dal: cur_dal = Depends(get_current_dal)):
    """ Create order detail """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Order details name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def update_orderdetail(pid: int, payload: data_in,
                             dal: cur_dal = Depends(get_current_dal)):
    """ Update order detail by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Order details name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_orderdetail(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete order detail by id """
    return await dal.remove(pid)
