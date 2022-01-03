""" Stock Schema """

from src.models.base_model import CamelModel

class FirstStockIn(CamelModel):
    """ router parameter in """
    product_id: int
    unit_id: int
    qty: float
    unit_name: str
    content: float

class FirstStockOut(FirstStockIn):
    pass
