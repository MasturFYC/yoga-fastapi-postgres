""" Product Schema """

from typing import Optional
from src.models.base_model import CamelModel

class ProductIn(CamelModel):
    """ product Camel Model """
    category_id: int
    name: str
    spec: Optional[str] = None  # pylint: disable=unsubscriptable-object
    base_unit: str
    base_price: float = 0
    base_weight: float = 0
    first_stock: float = 0
    stock: float = 0
    is_active: bool = True
    is_sale: bool = True


class ProductOut(ProductIn):
    """ product Camel Model """
    id: int
