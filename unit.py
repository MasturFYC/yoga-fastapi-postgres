
"""
Tabel unit with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from base import Base

# from sqlalchemy.sql.schema import PrimaryKeyConstraint


class Unit(Base):
    """ Tabel units base model """
    __tablename__ = 'units'
    __table_args__ = (
        UniqueConstraint(
            'product_id',
            'name',
            name='uq_unit_name'
        ),
    )

    product_id = Column(SmallInteger, ForeignKey("products.id"), index=True)
    id = Column(Integer, Sequence('units_id_seq'), primary_key=True, index=True)
    name = Column(String(6), nullable=False, index=True)
    content = Column(Numeric(8, 2), nullable=False, default=0)
    buy_price = Column(Numeric(12, 2), nullable=False, default=0)
    margin = Column(Numeric(5, 4), nullable=False, default=0)
    price = Column(Numeric(12, 2), nullable=False, default=0)
    is_default = Column(Boolean, nullable=False, default=False)
    product = relationship("product.Product", back_populates="units")

    def __init__(self, product_id, name, content, price, buy_price, margin, is_default):
        self.product_id = product_id
        self.name = name
        self.content = content
        self.price = price
        self.buy_price = buy_price
        self.margin = margin
        self.is_default = is_default
