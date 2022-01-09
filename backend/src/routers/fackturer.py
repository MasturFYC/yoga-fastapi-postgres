""" Fackturer Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.schemas.fackturer import FackturerIn as data_in, FackturerOut as data_out
from src.dals.fackturer import FackturerDal as cur_dal


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/api/fackturers",
    tags=["fackturers"],
    responses={404: {"Fackturer": "Not found"}},
)


@ROUTER.get("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def read_fackturer(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get fackturer by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Fackturer not found")

    return res.__dict__


@ROUTER.get("/", response_model=List[data_out], status_code=status.HTTP_200_OK)
async def read_fackturers(skip: int = 0, take: int = 20, dal: cur_dal = Depends(get_current_dal)):
    """ Get all fackturers """
    res = await dal.get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Fackturer is empty")
    return [row.__dict__ for row in res]

@ROUTER.post("/", response_model=data_out, status_code=status.HTTP_201_CREATED)
async def create_fackturer(payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Create fackturer """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Fackturer name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def update_fackturer(pid: int, payload: data_in, dal: cur_dal = Depends(get_current_dal)):
    """ Update fackturer by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Fackturer name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_fackturer(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete fackturer by id """
    return await dal.remove(pid)
