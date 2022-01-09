""" FackturerDetail Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.dals.fackturerdetail import FackturerDetailDal as cur_dal
from src.schemas.fackturerdetail import FackturerDetailIn as data_in,\
    FackturerDetailOut as data_out


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)

ROUTER = APIRouter(
    prefix="/api/fackturerdetails",
    tags=["fackturerdetails"],
    responses={404: {"Fackturer Detail": "Not found"}},
)


@ROUTER.get("/fackturer/{pid}",
            response_model=List[data_out],
            status_code=status.HTTP_200_OK)
async def read_fackturerdetails(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get fackturer details by fackturer """
    res = await dal.get_by_fackturer(pid)
    if res is None:
        raise HTTPException(
            status_code=404, detail="Fackturer details is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def read_fackturerdetail(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get fackturer detail by id """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(
            status_code=404, detail="Fackturer details is empty")
    return res.__dict__


@ROUTER.post("/", response_model=data_out, status_code=status.HTTP_201_CREATED)
async def create_fackturerdetail(payload: data_in,
                                 dal: cur_dal = Depends(get_current_dal)):
    """ Create fackturer detail """
    res = await dal.create(payload)

    if res is None:
        raise HTTPException(
            status_code=500, detail="Fackturer details name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=data_out, status_code=status.HTTP_200_OK)
async def update_fackturerdetail(pid: int, payload: data_in,
                                 dal: cur_dal = Depends(get_current_dal)):
    """ Update fackturer detail by id """
    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(
            status_code=500, detail="Fackturer details name exist")

    return res.__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_fackturerdetail(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete fackturer detail by id """
    return await dal.remove(pid)
