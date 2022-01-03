"""
Tabel Customer Order with model
"""

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Sequence, DateTime, Column, Integer, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL
from src.models.base_model import declare_base


class CustomerOrder(declare_base):
    """ Tabel Customer Order base model """
    __tablename__ = 'orders'

    id = Column(Integer,
                server_default=Sequence(
                    'order_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=Integer).next_value(),
                primary_key=True)
    total = Column(DECIMAL(12, 2), nullable=False, default=0)
    cash = Column(DECIMAL(12, 2), nullable=False, default=0)
    payment = Column(DECIMAL(12, 2), nullable=False, default=0)
    remain_payment = Column(DECIMAL(12, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=sa.func.now(),
                        default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True),
                        server_default=sa.func.now(),
                        nullable=False,
                        default=datetime.utcnow())

    customer_id = Column(SmallInteger, ForeignKey(
        "customers.id"), index=True, nullable=False)
    sales_id = Column(SmallInteger, ForeignKey(
        "salesmans.id"), index=True, nullable=False)

    customer = relationship(
        "src.models.customer.Customer", back_populates='orders')

    salesman = relationship(
        "src.models.salesman.Salesman", back_populates='orders')

    order_details = relationship(
        "src.models.orderdetail.OrderDetail", back_populates='customer_order')

    def __init__(self, **kwargs):
        valid_keys = ["customer_id", "sales_id", "total", "cash",
                      "payment", "remain_payment", "created_at", "updated_at"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
