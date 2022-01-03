"""
Tabel Order Details with model
"""

from sqlalchemy import Sequence, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL
from src.models.base_model import declare_base


class OrderDetail(declare_base):
    """ Tabel Order Detail base model """
    __tablename__ = 'order_details'

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
    buy_price = Column(DECIMAL(12, 2), nullable=False, default=0)
    discount = Column(DECIMAL(12, 2), nullable=False, default=0)
    subtotal = Column(DECIMAL(12, 2), nullable=False, default=0)
    
    order_id = Column(Integer,
                      ForeignKey("orders.id", ondelete='CASCADE'),
                      index=True, nullable=False)
    product_id = Column(Integer,
                        ForeignKey("products.id"),
                        nullable=False, index=True)
    unit_id = Column(Integer,
                     ForeignKey("units.id"),
                     nullable=False, index=True)

    customer_order = relationship("src.models.customerorder.CustomerOrder",
                         back_populates='order_details')

    product = relationship("src.models.product.Product",
                           back_populates='order_details')

    unit = relationship("src.models.unit.Unit",
                        back_populates='order_details')

    def __init__(self, **kwargs):
        valid_keys = ["order_id", "product_id", "unit_id", "qty",
                      "content", "unit_name", "real_qty", "price", 
                      "buy_price", "discount", "subtotal"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
