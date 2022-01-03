"""
Tabel Salesman with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, String
from sqlalchemy.orm import relationship
from src.models.base_model import declare_base


class Salesman(declare_base):
    """ Tabel Salesman base model """
    __tablename__ = 'salesmans'
    id = Column('id', SmallInteger,
                server_default=Sequence(
                    'salesman_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=SmallInteger).next_value(),
                primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    street = Column(String(128), nullable=False)
    city = Column(String(50), nullable=False)
    phone = Column(String(25), nullable=False)
    cell = Column(String(25), nullable=True)
    zip = Column(String(8), nullable=True)
    email = Column(String(128), nullable=True)

    orders = relationship(
        "src.models.customerorder.CustomerOrder", back_populates="salesman")

    def __repr__(self):
        return '<test_result: {}>'.format(self.name)
