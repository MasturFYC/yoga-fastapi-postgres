""" StockDetail Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.dals.unit import UnitDal
from src.schemas.unit import UnitIn, UnitOut


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield UnitDal(session)


ROUTER = APIRouter(
    prefix="/api/units",
    tags=["units"],
    responses={404: {"units": "Not found"}},
)


@ROUTER.get("/product/{pid}",
            response_model=List[UnitOut],
            status_code=status.HTTP_200_OK)
async def read_by_product(pid: int, dal: UnitDal = Depends(get_current_dal)):
    """ Get units by stock """
    res = await dal.unit_get_by_product(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Units is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=UnitOut, status_code=status.HTTP_200_OK)
async def read_unit(pid: int, dal: UnitDal = Depends(get_current_dal)):
    """ Get unit by id """
    res = await dal.unit_get_one(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Units is empty")
    return res.__dict__


@ROUTER.post("/", response_model=UnitOut, status_code=status.HTTP_201_CREATED)
async def create_unit(payload: UnitIn,
                      dal: UnitDal = Depends(get_current_dal)):
    """ Create unit """
    res = await dal.unit_insert(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Unit name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=UnitOut, status_code=status.HTTP_200_OK)
async def update_unit(pid: int, payload: UnitIn,
                      dal: UnitDal = Depends(get_current_dal)):
    """ Update unit by id """
    res = await dal.unit_update(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Unit name exist")

    return res #.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_unit(pid: int, dal: UnitDal = Depends(get_current_dal)):
    """ Delete unit by id """
    return await dal.unit_delete(pid)
