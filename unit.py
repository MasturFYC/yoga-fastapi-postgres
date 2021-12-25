from enum import unique
from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from base import Base

class Unit(Base):
    __tablename__ = 'units'

    product_id = Column(SmallInteger, ForeignKey("products.id"), unique=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(6), nullable=False, unique=True)
    content = Column(Numeric(8, 2), nullable=False, default=0)
    price = Column(Numeric(12, 2), nullable=False, default=0)
    buy_price = Column(Numeric(12, 2), nullable=False, default=0)
    margin = Column(Numeric(5, 4), nullable=False, default=0)
    is_default = Column(Boolean, nullable=False, default=False)
    product = relationship("Product", back_populates="units")

    def __init__(self, product_id, id, name, content, price, buy_price, margin, is_default):
        self.product_id = product_id
        self.id = id
        self.name = name
        self.content = content
        self.price = price
        self.buy_price = buy_price
        self.margin = margin
        self.is_default = is_default
