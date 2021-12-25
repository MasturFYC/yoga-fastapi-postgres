from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    # code = Column(String(8), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    spec = Column(String(128), nullable=True)
    unit = Column(String(6), nullable=False)
    # base_unit = Column(String(6), nullable=False)
    #base_weight = Column(Numeric(10, 2), nullable=False, default=0)
    price = Column(Numeric(12, 2), nullable=False, default=0)
    # base_price = Column(Numeric(12, 2), nullable=False, default=0)
    update_notif = Column(Boolean, nullable=False, default=False)
    stock = Column(Numeric(10, 2), nullable=False, default=0)
    first_stock = Column(Numeric(10, 2), nullable=False, default=0)
    # unit_in_stock = Column(Numeric(10, 2), nullable=False, default=0)
    category_id = Column(SmallInteger, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    units = relationship("Unit", back_populates="product")


    def __init__(self,
                 # code,
                 # base_unit,
                 # base_price,
                 # base_weight,
                 # is_active
                 # unit_int_stock
                 name,
                 spec,
                 price,
                 update_notif,
                 first_stock,
                 stock,
                 category_id):
        # self.code = code
        self.name = name
        self.spec = spec
        #self.base_unit = base_unit
        #self.base_weight = base_weight
        #self.base_price = base_price
        #self.is_active = is_active
        self.price = price
        self.first_stock = first_stock
        #self.unit_in_stock = unit_int_stock
        self.stock = stock
        self.update_notif = update_notif
        self.category_id = category_id
