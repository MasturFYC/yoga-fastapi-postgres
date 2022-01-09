""" Category Router """
from typing import List
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from src.dals.category import CategoryDal as cur_dal
from src.schemas.category import CategoryIn, CategoryOut
from src.models.base_model import db_session


async def get_current_dal():
    ''' middleware '''
    async with db_session() as session:
        async with session.begin():
            yield cur_dal(session)


ROUTER = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    responses={404: {"categories": "Not found"}},
)


@ROUTER.get("/", response_model=List[CategoryOut],
            status_code=status.HTTP_200_OK)
async def read_categories(skip: int = 0, take: int = 20,
                          dal: cur_dal = Depends(get_current_dal)):
    """ Get all categories """
    res = await dal.get_all(skip, take)
    if res is None:
        raise HTTPException(status_code=404, detail="Category is empty")

    return [row.__dict__ for row in res]


@ROUTER.get("/{pid}/",
            response_model=CategoryOut,
            status_code=status.HTTP_200_OK)
async def read_category(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Get one category """
    res = await dal.get_one(pid)
    if res is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return res.__dict__


@ ROUTER.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryIn,
                          dal: cur_dal = Depends(get_current_dal)):
    """ create new category """
    
    res = await dal.create(payload)

    # print('----------', res.id, '----------', res.name)

    if res is None:
        raise HTTPException(status_code=500, detail="Category name exist")

    return res.__dict__


@ ROUTER.put("/{pid}/", response_model=CategoryOut, status_code=status.HTTP_200_OK)
async def update_category(pid: int, payload: CategoryIn,
                          dal: cur_dal = Depends(get_current_dal)):
    """ Update category by id """
    # print('--------------',payload)

    res = await dal.modify(pid, payload)

    if res is None:
        raise HTTPException(status_code=500, detail="Category name exist")

    return res #.__dict__


@ ROUTER.delete("/{pid}/", status_code=status.HTTP_200_OK)
async def delete_category(pid: int, dal: cur_dal = Depends(get_current_dal)):
    """ Delete category by id """
    return await dal.remove(pid)
