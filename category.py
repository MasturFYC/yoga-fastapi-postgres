"""
Tabel category with model
"""

from sqlalchemy import Sequence, Column, SmallInteger, String
from sqlalchemy.orm import relationship
from base import Base


class Category(Base):
    """ Tabel categories base model """
    __tablename__ = 'categories'

    id = Column(SmallInteger, Sequence("categories_id_seq"), primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("product.Product", back_populates="category")

    def __init__(self, name):
        self.name = name
