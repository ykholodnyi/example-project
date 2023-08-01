import enum

from sqlalchemy import (
    Column, String, DateTime, Integer, ForeignKey,
    and_, or_, text
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, ENUM as PG_ENUM

from app.models.base import Base, SessionLocal


class BookingStatusEnum(enum.Enum):
    HOLD = "HOLD"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    machine_code = Column(String)
    calendar_event_id = Column(String)
    status = Column(PG_ENUM(BookingStatusEnum), default=BookingStatusEnum.HOLD.value)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    study_id = Column(Integer, ForeignKey('studies.id'))

    study = relationship('Study', back_populates='bookings')

    @classmethod
    def overlapping_bookings_exists(
        cls,
        machine_code: str,
        start_time: DateTime,
        end_time: DateTime,
        session: SessionLocal,
        **kwargs
    ) -> bool:
        return session.execute(
            text(
                "SELECT EXISTS ("
                "SELECT 1 FROM bookings "
                "WHERE tsrange(start_time, end_time, '()') && tsrange(:new_start, :new_end, '()')"
                "AND machine_code = :machine_code)"
            ),
            {"new_start": start_time, "new_end": end_time, "machine_code": machine_code},
        ).scalar()
