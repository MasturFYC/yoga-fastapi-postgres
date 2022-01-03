""" Unit Schema """

from src.models.base_model import CamelModel


class UnitIn(CamelModel):
    """ unit Camel Model """
    product_id: int
    name: str
    content: float
    buy_price: float
    margin: float
    price: float
    is_default: bool


class UnitOut(UnitIn):
    """ unit camel Model """
    id: int
