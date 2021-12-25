from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship
from base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("Product", back_populates="category")

    def __init__(self, name):
        self.name = name
