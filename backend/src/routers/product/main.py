""" Product Router """

from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from src.models.base_model import db_session
from src.schemas.product import ProductIn as py_in, ProductOut as py_out
from src.dals.product import ProductDal as cur_dal


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)

ROUTER = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"products": "Not found"}},
)


@ROUTER.get("/", response_model=List[py_out], status_code=status.HTTP_200_OK)
async def read_products(skip: int = 0, take: int = 20, dal: cur_dal = Depends(get_current_dal)):
    """ Get all products """
    res = await dal.product_get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Product is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/search/{name}/", response_model=List[py_out], status_code=status.HTTP_200_OK)
async def search_products(name: str, dal: cur_dal = Depends(get_current_dal)):
    """ Search products by name """
    res = await dal.search_name(name)
    if res is None:
        raise HTTPException(status_code=404, detail="Product is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/category/{pid}/", response_model=List[py_out], status_code=status.HTTP_200_OK)
async def get_by_category(pid: int = 0, dal: cur_dal = Depends(get_current_dal)):
    """ Search products by name """
    res = await dal.get_by_category(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Product is empty")
    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/", response_model=py_out, status_code=status.HTTP_200_OK)
async def read_product(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get product by id """
    res = await dal.product_get_one(pid)

    if res is None:
        raise HTTPException(status_code=500, detail="Product not found")

    return res.__dict__


@ROUTER.post("/", response_model=py_out, status_code=status.HTTP_201_CREATED)
async def create_products(payload: py_in, dal: cur_dal = Depends(get_current_dal)):
    """ Create product """
    res = await dal.product_insert(payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Product name exist")

    return res.__dict__


@ROUTER.put("/{pid}/", response_model=py_out, status_code=status.HTTP_200_OK)
async def update_product(pid: int, payload: py_in, dal: cur_dal = Depends(get_current_dal)):
    """ Update product by id """
    res = await dal.product_update(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Product name exist")

    return res  # .__dict__


@ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_product(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete product by id """
    return await dal.product_delete(pid)
