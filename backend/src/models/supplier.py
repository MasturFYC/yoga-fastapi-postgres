"""
Tabel Supplier with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, String
from sqlalchemy.orm import relationship
from src.models.base_model import declare_base


class Supplier(declare_base):
    """ Tabel Supplier base model """
    __tablename__ = 'suppliers'

    id = Column(SmallInteger,
                server_default=Sequence(
                    'supplier_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=SmallInteger).next_value(),
                primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    sales_name = Column(String(50), nullable=False)
    street = Column(String(128), nullable=False)
    city = Column(String(50), nullable=False)
    phone = Column(String(25), nullable=False)
    cell = Column(String(25), nullable=True)
    zip = Column(String(8), nullable=True)
    email = Column(String(128), nullable=True)

    stocks = relationship("src.models.stock.Stock", back_populates="supplier")

    def __init__(self, **kwargs):
        valid_keys = ["name", "sales_name", "street", "city",
                      "phone", "cell", "zip", "email"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
