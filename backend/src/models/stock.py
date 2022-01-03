"""
Tabel Stock with model
"""

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Sequence, DateTime, Column, Integer, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL, Numeric
from src.models.base_model import declare_base


class Stock(declare_base):
    """ Tabel Stock base model """
    __tablename__ = 'stocks'

    id = Column(Integer,
                server_default=Sequence(
                    'order_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=Integer).next_value(),
                primary_key=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
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

    supplier_id = Column(SmallInteger, ForeignKey(
        "suppliers.id"), index=True, nullable=False)

    supplier = relationship(
        "src.models.supplier.Supplier", back_populates='stocks')

    stock_details = relationship("src.models.stockdetail.StockDetail",
                                 back_populates="stock")

    def __init__(self, **kwargs):
        valid_keys = ["supplier_id", "invoice_number", "total", "cash",
                      "payment", "remain_payment", "created_at", "updated_at"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
