""" Stock Detail Schema """

from src.models.base_model import CamelModel


class StockDetailIn(CamelModel):
    """ router parameter in """
    qty: float
    content: float
    unit_name: str
    price: float
    discount: float
    stock_id: int
    product_id: int
    unit_id: int


class StockDetailOut(StockDetailIn):
    """ router parameter out """
    id: int
    real_qty: float
    subtotal: float
