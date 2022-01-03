""" Order Detail Schema """

from src.models.base_model import CamelModel


class OrderDetailIn(CamelModel):
    """ router parameter in """
    order_id: int
    product_id: int
    unit_id: int
    qty: float
    content: float
    unit_name: str
    price: float
    buy_price: float
    discount: float


class OrderDetailOut(OrderDetailIn):
    """ router parameter out """
    id: int
    real_qty: float
    subtotal: float
