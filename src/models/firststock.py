
"""
Tabel first_stock with model
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DECIMAL
from src.models.base_model import declare_base


class FirstStock(declare_base):
    """ Tabel first_stocks base model """
    __tablename__ = 'first_stocks'

    qty = Column(DECIMAL(10, 2), nullable=False, default=0)
    unit_name = Column(String(6), nullable=False)
    content = Column(DECIMAL(8, 2), nullable=False, default=0)

    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete='CASCADE'), primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"),
                     nullable=False, index=True)

    product = relationship('src.models.product.Product',
                           back_populates='first_stocks')

    unit = relationship('src.models.unit.Unit',
                        back_populates='first_stocks')

    def __init__(self, **kwargs):
        valid_keys = ["product_id", "unit_id", "qty", "unit_name", "content"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
