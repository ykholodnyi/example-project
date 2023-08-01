from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base


class Study(Base):
    __tablename__ = 'studies'
    id = Column(Integer, primary_key=True, index=True)
    patient = Column(String)
    bookings = relationship('Booking', back_populates='study')
