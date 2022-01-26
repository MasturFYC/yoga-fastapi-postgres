"""
Tabel category with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, String
from sqlalchemy.orm import relationship
from src.models.base_model import declare_base
from sqlalchemy import event


class Category(declare_base):  # pylint: disable = too-few-public-methods
    """ Tabel categories base model """

    __tablename__ = 'categories'

    id = Column(SmallInteger,
                server_default=Sequence(
                    'category_id_seq',
                    metadata=declare_base.metadata,
                    minvalue=1,
                    start=1,
                    data_type=SmallInteger).next_value(),
                primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    products = relationship("src.models.product.Product",
                             back_populates="category")

    def __init__(self, name):
        self.name = name
    
    def to_json(self):
        return dict(id=self.id, name=self.name)

def receive_after_update(mapper, connection, target):
    print("listen for the 'after_update' event--------------", mapper, connection, target)


event.listen(Category,  'after_update', receive_after_update)
