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


class ProductOut(CamelModel):
    id: int
    # code: str
    name: str
    spec: Optional[str] = None  # pylint: disable=unsubscriptable-object
    unit: str
    # base_unit: str
    # base_weight: float
    # base_price: float
    price: float
    # is_active: bool
    update_notif: bool
    first_stock: float
    # unit_in_stock: float
    stock: float
    category_id: int


class UnitIn(CamelModel):
    name: str


class UnitOut(CamelModel):
    product_id: int
    id: int
    name: str
    content: float
    price: str
    buy_price: float
    margin: float
    is_default: bool
    