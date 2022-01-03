""" salesman Router """
from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.schemas.salesman import SalesmanIn as data_in, SalesmanOut as data_out
from src.dals.salesman import SalesmanDal as cur_dal


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/salesmans",
    tags=["salesmans"],
    responses={404: {"salesman": "Not found"}},
)


@ROUTER.get("/", response_model=List[data_out], status_code=status.HTTP_200_OK)
async def reads(skip: int = 0, take: int = 20, dal: cur_dal = Depends(get_current_dal)):
    """ Get all salesmans """
    res = await dal.get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Salesman is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def read(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get salesman by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Salesman not found")

    return res.__dict__


@ROUTER.post("/", response_model=data_out, status_code=status.HTTP_201_CREATED)
async def create(payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Create salesman """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Salesman name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def modify(pid: int, payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Update salesman by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Salesman name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def remove(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete salesman by id """
    return await dal.remove(pid)
