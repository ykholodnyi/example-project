import logging

import graphene
from sqlalchemy import text

from app.graphql.exceptions import DefaultGQLError, ErrorCodes
from app.graphql.types.booking import (
    BookingType, BookingCreateInputType, BookingUpdateInputType,
)

from app.models import Booking
from app.graphql.mixins import CRUMixin

logger = logging.getLogger(__name__)


class CreateBooking(graphene.Mutation, CRUMixin):
    class Arguments:
        booking = graphene.Argument(BookingCreateInputType, required=True)

    booking = graphene.Field(BookingType)

    @classmethod
    def mutate(cls, root, info, booking, **kwargs):
        session = info.context["request"].state.db

        # lock the table, it would be released at the end of the transaction
        # also gist constraint with tsrange can be used, but can cause deadlocks
        session.execute(text('LOCK TABLE bookings IN EXCLUSIVE MODE;'))

        if Booking.overlapping_bookings_exists(**booking, session=session):
            error_str = "Booking overlaps with existing booking."
            logger.info(error_str)
            session.rollback()
            raise DefaultGQLError(
                error_str=error_str,
                extensions={"code": ErrorCodes.VALIDATION_ERROR.value})

        obj = Booking(**booking)
        obj = cls.add_object(obj=obj, session=session)

        return CreateBooking(booking=obj)


class UpdateBooking(graphene.Mutation, CRUMixin):
    class Arguments:
        booking = graphene.Argument(BookingUpdateInputType, required=True)

    booking = graphene.Field(BookingType)

    @classmethod
    def mutate(cls, root, info, booking, **kwargs):
        obj = cls.get_object(obj_id=booking.id, model=Booking, session=info.context["request"].state.db)
        obj = cls.update_object(obj, booking, session=info.context["request"].state.db)
        return UpdateBooking(booking=obj)
