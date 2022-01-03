"""
Tabel Stock Details with model
"""

from sqlalchemy import Sequence, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL
from src.models.base_model import declare_base


class StockDetail(declare_base):
    """ Tabel Stock Detail base model """
    __tablename__ = 'stock_details'

    id = Column(Integer, 
                server_default=Sequence(
                    'orderdetail_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=Integer).next_value(),
                primary_key=True)
    qty = Column(DECIMAL(10, 2), nullable=False, default=0)
    content = Column(DECIMAL(8, 2), nullable=False, default=0)
    unit_name = Column(String(6), nullable=False)
    real_qty = Column(DECIMAL(10, 2), nullable=False, default=0)
    price = Column(DECIMAL(12, 2), nullable=False, default=0)
    discount = Column(DECIMAL(12, 2), nullable=False, default=0)
    subtotal = Column(DECIMAL(12, 2), nullable=False, default=0)
    
    stock_id = Column(Integer,
                      ForeignKey("stocks.id", ondelete='CASCADE'),
                      index=True, nullable=False)
    product_id = Column(Integer,
                        ForeignKey("products.id"),
                        nullable=False, index=True)
    unit_id = Column(Integer,
                     ForeignKey("units.id"),
                     nullable=False, index=True)

    stock = relationship("src.models.stock.Stock",
                         back_populates='stock_details')

    product = relationship("src.models.product.Product",
                           back_populates='stock_details')

    unit = relationship("src.models.unit.Unit", back_populates='stock_details')

    def __init__(self, **kwargs):
        valid_keys = ["stock_id", "product_id", "unit_id", "qty",
                      "content", "unit_name", "real_qty", "price",
                      "discount", "subtotal"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
