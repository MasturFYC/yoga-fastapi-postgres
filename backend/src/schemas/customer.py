""" Customer Schema """

from typing import Optional
from src.models.base_model import CamelModel

class CustomerIn(CamelModel):
    """ router parameter in """
    name: str
    street: str
    city: str
    phone: str
    cell: Optional[str] # = None  # pylint: disable=unsubscriptable-object
    zip: Optional[str]  # = None  # pylint: disable=unsubscriptable-object
    email: Optional[str]  # = None  # pylint: disable=unsubscriptable-object


class CustomerOut(CustomerIn):
    """ router parameter out """
    id: int
