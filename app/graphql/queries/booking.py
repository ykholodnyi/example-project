import graphene
from sqlalchemy.orm import joinedload

from app.graphql.mixins import CRUMixin
from app.graphql.types.booking import BookingType
from app.models import Booking


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
        session = info.context["request"].state.db
        return session.query(Booking).options(joinedload(Booking.study)).all()
