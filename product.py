"""
Tabel product with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Product(Base):
    """ Tabel product base model """
    __tablename__ = 'products'

    id = Column(Integer, Sequence('products_id_seq'), primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    spec = Column(String(128), nullable=True)
    base_unit = Column(String(6), nullable=False)
    base_weight = Column(Numeric(10, 2), nullable=False, default=0)
    base_price = Column(Numeric(12, 2), nullable=False, default=0)
    first_stock = Column(Numeric(10, 2), nullable=False, default=0)
    stock = Column(Numeric(10, 2), nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=False)
    category_id = Column(SmallInteger, ForeignKey("categories.id"))
    category = relationship("category.Category", back_populates="products")
    units = relationship("unit.Unit", back_populates="product")


    def __init__(self,
                 name,
                 spec,
                 base_unit,
                 base_price,
                 base_weight,
                 is_active,
                 first_stock,
                 stock,
                 category_id):
        self.name = name
        self.spec = spec
        self.base_unit = base_unit
        self.base_weight = base_weight
        self.base_price = base_price
        self.is_active = is_active
        self.base_price = base_price
        self.first_stock = first_stock
        self.stock = stock
        self.category_id = category_id
