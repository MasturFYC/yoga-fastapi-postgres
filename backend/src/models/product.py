"""
Tabel product with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DECIMAL
from src.models.base_model import declare_base


class Product(declare_base):  # pylint: disable=too-few-public-methods
    """ Tabel product base model """
    __tablename__ = 'products'

    id = Column(Integer,
                server_default=Sequence(
                    'product_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=Integer).next_value(),
                primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    spec = Column(String(128), nullable=True)
    base_unit = Column(String(6), nullable=False)
    base_weight = Column(DECIMAL(10, 2), nullable=False, default=0)
    base_price = Column(DECIMAL(12, 2), nullable=False, default=0)
    first_stock = Column(DECIMAL(10, 2), nullable=False, default=0)
    stock = Column(DECIMAL(10, 2), nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    is_sale = Column(Boolean, nullable=False, default=False)

    category_id = Column(SmallInteger, ForeignKey("categories.id"), nullable=False, default=0)

    category = relationship(
        "src.models.category.Category", back_populates="products")

    units = relationship("src.models.unit.Unit",
                         back_populates="product")

    first_stocks = relationship("src.models.firststock.FirstStock",
                                back_populates="product")

    stock_details = relationship("src.models.stockdetail.StockDetail",
                                 back_populates="product")

    order_details = relationship("src.models.orderdetail.OrderDetail",
                                 back_populates="product")

    fackturer_details = relationship("src.models.fackturerdetail.FackturerDetail",
                                 back_populates="product")

    def __init__(self, **kwargs):
        valid_keys = ["name", "spec", "base_unit", "base_weight",
                      "base_price", "first_stock", "stock",
                      "is_active", "is_sale", "category_id"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
