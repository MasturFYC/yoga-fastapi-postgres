""" Customer Order Schema """

from datetime import datetime
from typing import Optional
from pydantic import validator
from src.models.base_model import CamelModel

class FackturerIn(CamelModel):
    """ schema parameter in """
    name: str
    descriptions: Optional[str] = None
    instructions: Optional[str] = None
    qty: float
    created_at: datetime = None

    @classmethod
    @validator("created_at", pre=True)
    def stock_date_validate(cls, value) -> None:
        ''' DOC STRING '''
        return datetime.fromtimestamp(value)


class FackturerOut(FackturerIn):
    """ schema parameter out """
    id: int
    price: float
    total: float
    updated_at: datetime = None

    @classmethod
    @validator("updated_at", pre=True)
    def updated_at_validate(cls, value) -> None:
        ''' DOC STRING '''
        return datetime.fromtimestamp(value)
