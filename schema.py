from typing import Optional
from base import CamelModel


class NoteIn(CamelModel):
    text: str
    completed: bool


class NoteOut(CamelModel):
    id: int
    text: str
    completed: bool


class CategoryIn(CamelModel):
    name: str


class CategoryOut(CamelModel):
    id: int
    name: str


class ProductIn(CamelModel):
    name: str
    spec: Optional[str] = None  # pylint: disable=unsubscriptable-object
    base_unit: str
    base_price: float
    base_weight: float
    first_stock: float
    stock: float
    category_id: int
    is_active: bool


class ProductOut(CamelModel):
    id: int
    name: str
    spec: Optional[str] = None  # pylint: disable=unsubscriptable-object
    base_unit: str
    base_price: float
    base_weight: float
    first_stock: float
    stock: float
    category_id: int
    is_active: bool


class UnitIn(CamelModel):
    product_id: int
    name: str
    content: float
    buy_price: float
    margin: float
    price: str
    is_default: bool


class UnitOut(CamelModel):
    product_id: int
    id: int
    name: str
    content: float
    buy_price: float
    margin: float
    price: str
    is_default: bool
