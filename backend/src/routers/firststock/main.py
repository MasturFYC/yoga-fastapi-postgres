""" StockDetail Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.dals.firststock import FirstStockDal as cur_dal
from src.schemas.firststock import FirstStockIn as fs_in, FirstStockOut as fs_out


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/api/firststocks",
    tags=["firststocks"],
    responses={404: {"Stock Detail": "Not found"}},
)


@ROUTER.get("/product/{pid}",
            response_model=List[fs_out],
            status_code=status.HTTP_200_OK)
async def read_firststocks(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get first stock by stock """
    res = await dal.firststock_get_one(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="First stock is empty")
    return [row.__dict__ for row in res]


@ROUTER.post("/", response_model=fs_out, status_code=status.HTTP_201_CREATED)
async def create_firststock(payload: fs_in,
                            dal: cur_dal = Depends(get_current_dal)):
    """ Create first stock """
    res = await dal.firststock_insert(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="First stock name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=fs_out, status_code=status.HTTP_200_OK)
async def update_firststock(pid: int, payload: fs_in,
                            dal: cur_dal = Depends(get_current_dal)):
    """ Update first stock by id """
    res = await dal.firststock_update(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="First stock name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_firststock(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete first stock by id """
    return await dal.firststock_delete(pid)
