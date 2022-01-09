""" Supplier Router """
from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.schemas.supplier import SupplierIn, SupplierOut
from src.dals.supplier import SupplierDal as cur_dal

async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/api/suppliers",
    tags=["suppliers"],
    responses={404: {"Supplier": "Not found"}},
)


@ROUTER.get("/", response_model=List[SupplierOut], status_code=status.HTTP_200_OK)
async def read_suppliers(skip: int = 0, take: int = 20, dal: cur_dal=Depends(get_current_dal)):
    """ Get all suppliers """
    res = await dal.supplier_get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Supplier is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=SupplierOut, status_code=status.HTTP_200_OK)
async def read_supplier(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get supplier by id """
    res = await dal.supplier_get_one(pid)
    if res is None:
        raise HTTPException(status_code=500, detail="Supplier not found")

    return res.__dict__


@ROUTER.post("/", response_model=SupplierOut, status_code=status.HTTP_201_CREATED)
async def create_supplier(payload: SupplierIn, dal: cur_dal = Depends(get_current_dal)):
    """ Create supplier """
    res = await dal.supplier_insert(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Supplier name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=SupplierOut, status_code=status.HTTP_200_OK)
async def update_supplier(pid: int, payload: SupplierIn, dal: cur_dal = Depends(get_current_dal)):
    """ Update supplier by id """
    res = await dal.supplier_update(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Supplier name exist")

    return res #.__dict__

@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_supplier(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete supplier by id """
    return await dal.supplier_delete(pid)
 
