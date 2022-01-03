""" Fackturer Detail Schema """

from src.models.base_model import CamelModel


class FackturerDetailIn(CamelModel):
    """ router parameter in """
    facturer_id: int
    product_id: int
    unit_id: int
    qty: float
    content: float
    unit_name: str
    price: float


class FackturerDetailOut(FackturerDetailIn):
    """ router parameter out """
    id: int
    real_qty: float
    subtotal: float
