
"""
Tabel unit with model
"""

from sqlalchemy import Sequence, Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from src.models.base_model import declare_base

# from sqlalchemy.sql.schema import PrimaryKeyConstraint


class Unit(declare_base):
    """ Tabel units base model """
    __tablename__ = 'units'
    __table_args__ = (
        UniqueConstraint(
            'product_id',
            'name',
            name='uq_unit_name'
        ),
    )

    id = Column(Integer,
                server_default=Sequence(
                    'unit_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=Integer).next_value(),
                primary_key=True)
    name = Column(String(6), nullable=False, index=True)
    content = Column(DECIMAL(8, 2), nullable=False, default=0)
    buy_price = Column(DECIMAL(12, 2), nullable=False, default=0)
    margin = Column(DECIMAL(8, 4), nullable=False, default=0)
    price = Column(DECIMAL(12, 2), nullable=False, default=0)
    is_default = Column(Boolean, nullable=False, default=False)

    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete='CASCADE'), index=True, nullable=False)

    product = relationship("src.models.product.Product",
                           back_populates="units")

    first_stocks = relationship("src.models.firststock.FirstStock",
                                back_populates="unit")

    stock_details = relationship("src.models.stockdetail.StockDetail",
                                 back_populates="unit")

    order_details = relationship("src.models.orderdetail.OrderDetail",
                                 back_populates="unit")

    fackturer_details = relationship("src.models.fackturerdetail.FackturerDetail",
                                 back_populates="unit")

    def __init__(self, **kwargs):
        valid_keys = ["product_id", "name", "content",
                      "price", "buy_price", "margin", "is_default"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
