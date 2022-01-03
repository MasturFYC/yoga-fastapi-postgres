""" StockDetail Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.dals.stockdetail import StockDetailDal
from src.schemas.stockdetail import StockDetailIn, StockDetailOut


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield StockDetailDal(session)


ROUTER = APIRouter(
    prefix="/stockdetails",
    tags=["stockdetails"],
    responses={404: {"Stock Detail": "Not found"}},
)


@ROUTER.get("/stock/{pid}",
            response_model=List[StockDetailOut],
            status_code=status.HTTP_200_OK)
async def read_stockdetails(pid: int, dal: StockDetailDal = Depends(get_current_dal)):
    """ Get stock details by stock """
    res = await dal.get_by_stock(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Stock Details is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=StockDetailOut, status_code=status.HTTP_200_OK)
async def read_stockdetail(pid: int, dal: StockDetailDal = Depends(get_current_dal)):
    """ Get stock detail by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Stock Details is empty")
    return res.__dict__


@ROUTER.post("/", response_model=StockDetailOut, status_code=status.HTTP_201_CREATED)
async def create_stockdetail(payload: StockDetailIn,
                             dal: StockDetailDal = Depends(get_current_dal)):
    """ Create stock detail """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Stock Details name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=StockDetailOut, status_code=status.HTTP_200_OK)
async def update_stockdetail(pid: int, payload: StockDetailIn,
                             dal: StockDetailDal = Depends(get_current_dal)):
    """ Update stock detail by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Stock Details name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_stockdetail(pid: int, dal: StockDetailDal = Depends(get_current_dal)):
    """ Delete stock detail by id """
    return await dal.remove(pid)
