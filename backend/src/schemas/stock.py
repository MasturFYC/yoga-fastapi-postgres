""" Stock Schema """

from datetime import datetime, timedelta, timezone
from pydantic import validator
from src.models.base_model import CamelModel
import pytz

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
    def parse_created_at(cls, value):
        ''' DOC STRING '''
        return datetime.fromtimestamp(value, pytz.timezone('Asia/Jakarta'))

class StockOut(StockIn):
    """ router parameter out """
    id: int
    updated_at: datetime = None

    @classmethod
    @validator("updated_at", pre=True)
    def parse_updated_at(cls, value) -> None:
        ''' DOC STRING '''
        return datetime.fromtimestamp(value, pytz.timezone('Asia/Jakarta'))
