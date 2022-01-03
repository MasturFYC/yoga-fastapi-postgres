"""
Tabel Fackturer with model
"""

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Sequence, DateTime, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DECIMAL
from src.models.base_model import declare_base


class Fackturer(declare_base):
    """ Tabel Fackturer base model """
    __tablename__ = 'fackturers'

    id = Column(Integer,
                server_default=Sequence(
                    'order_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=Integer).next_value(),
                primary_key=True)
    name = Column(String(50), nullable=False)
    descriptions = Column(String(128), nullable=True)
    instructions = Column(String(512), nullable=True)
    total = Column(DECIMAL(12, 2), nullable=False, default=0)
    qty = Column(DECIMAL(12, 2), nullable=False, default=0)
    price = Column(DECIMAL(12, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=sa.func.now(),
                        default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True),
                        nullable=False,
                        default=datetime.utcnow(),
                        server_default=sa.func.now())

    fackturer_details = relationship(
        "src.models.fackturerdetail.FackturerDetail", back_populates='fackturer')

    def __init__(self, **kwargs):
        valid_keys = ["name", "descriptions", "inistructions", "total",
                      "qty", "price", "created_at", "updated_at"]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
