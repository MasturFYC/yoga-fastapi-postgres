from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class Notes(Base):
    __tablename__ = 'notes'

    id = Column(SmallInteger, primary_key=True, index=True)
    text = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return "<notes(name='%s')>" % (self.text)