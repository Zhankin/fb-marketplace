from sqlalchemy import Column, String, Integer, Text
from db.base import Base


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    query = Column(Text, unique=False, nullable=False)
    name = Column(String(255), unique=False, nullable=False)
    price = Column(String(255), unique=False, nullable=False)
    image = Column(Text, unique=False, nullable=False)
    link = Column(Text, unique=False, nullable=False)

    def __init__(self, query, name, price, image, link):
        self.query = query
        self.name = name
        self.price = price
        self.image = image
        self.link = link
