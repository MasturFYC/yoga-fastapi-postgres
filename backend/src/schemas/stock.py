""" Stock Schema """

from datetime import datetime
from pydantic import validator
from src.models.base_model import CamelModel

class StockIn(CamelModel):
    """ router parameter in """
    supplier_id: int
    invoice_number: str
    total: float
    cash: float
    payment: float
    remain_payment: float
    created_at: datetime = None

    @classmethod
    @validator("created_at", pre=True)
    def stock_date_validate(cls, value) -> None:
        ''' DOC STRING '''
        return datetime.fromtimestamp(value)


class StockOut(StockIn):
    """ router parameter out """
    id: int
    updated_at: datetime = None

    @classmethod
    @validator("updated_at", pre=True)
    def updated_at_validate(cls, value) -> None:
        ''' DOC STRING '''
        return datetime.fromtimestamp(value)
