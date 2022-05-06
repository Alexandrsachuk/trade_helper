from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from trade.database import Base
from datetime import date

class Pair_history(Base):
    __tablename__ = 'pair_history'

    id = Column(Integer, primary_key=True)
    open_date = Column(Date)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    pair_name = Column(String)

    def __init__(self, open_date: date, open_price: float, high_price: float, low_price: float, close_price: float,
                 volume: float, pair_name: str):
        self.open_date = open_date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.pair_name = pair_name

    def __repr__(self):
        return f'{self.close_price}'
