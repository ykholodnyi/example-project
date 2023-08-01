import datetime

import graphene
from sqlalchemy.orm import joinedload

from app.graphql.mixins import CRUMixin
from app.graphql.types.booking import BookingType
from app.models import Booking, Study
from app.models.booking import BookingStatusEnum


class BookingQuery(CRUMixin):
    booking = graphene.Field(
        BookingType,
        booking_id=graphene.ID())

    bookings = graphene.List(BookingType)

    @classmethod
    def resolve_booking(cls, _, info, booking_id):
        return cls.get_object(obj_id=booking_id, model=Booking, session=info.context["request"].state.db)

    @classmethod
    def resolve_bookings(cls, _, info):
        import random
        session = info.context["request"].state.db
        # Create 10 studies
        for i in range(10):
            study = Study(patient=str(i))
            session.add(study)
            session.commit()

            # Create 2 bookings for each study
            for j in range(2):
                machine_code = f'machine_{j}'
                calendar_event_id = f'event_{j}'
                status = random.choice([status.value for status in BookingStatusEnum])
                start_time = datetime.datetime(2023, 1, 1, 1, 0, 0)
                end_time = start_time + datetime.timedelta(hours=1)

                booking = Booking(
                    machine_code=machine_code,
                    calendar_event_id=calendar_event_id,
                    status=status,
                    start=start_time,
                    end=end_time,
                    study_id=study.id
                )
                session.add(booking)

            session.commit()

        return session.query(Booking).options(
            joinedload(Booking.study),
        ).all()
