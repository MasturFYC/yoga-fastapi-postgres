""" Category Router """
from typing import List
from fastapi import APIRouter, status
from sqlalchemy import select, update, insert, delete
from base import database
from category import Category
from schema import CategoryIn, CategoryOut

ROUTER = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"categories": "Not found"}},
)


@ROUTER.get("/", response_model=List[CategoryOut], status_code=status.HTTP_200_OK)
async def read_categories(skip: int = 0, take: int = 20):
    """ Get all categories """
    query = select(Category).offset(skip).limit(take)
    return await database.fetch_all(query)


@ROUTER.get("/{cat_id}/", response_model=CategoryIn, status_code=status.HTTP_200_OK)
async def read_category(cat_id: int):
    """ Get one category """
    query = select(Category).where(Category.id == cat_id)
    return await database.fetch_one(query)


@ROUTER.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_categories(cat: CategoryIn):
    """ create new category """
    query = insert(Category).values(name=cat.name)
    last_record_id = await database.execute(query)
    return {**cat.dict(), "id": last_record_id}


@ROUTER.put("/{cat_id}/", response_model=CategoryOut, status_code=status.HTTP_200_OK)
async def update_category(cat_id: int, cat: CategoryIn):
    """ Update category by id """
    query = update(Category).where(Category.id == cat_id).values(name=cat.name)
    await database.execute(query)
    return {**cat.dict(), "id": cat_id}


@ROUTER.delete("/{cat_id}/", status_code=status.HTTP_200_OK)
async def delete_category(cat_id: int):
    """ Delete category by id """
    query = delete(Category).where(Category.id == cat_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(cat_id)}
