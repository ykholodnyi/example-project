import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.graphql.mixins import IDTypeMixin
from app.models.booking import Booking, BookingStatusEnum


BookingStatusEnumGraphene = graphene.Enum.from_enum(BookingStatusEnum)


class BookingType(SQLAlchemyObjectType, IDTypeMixin):
    class Meta:
        model = Booking
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection


class BookingCreateInputType(graphene.InputObjectType):
    machine_code = graphene.String(required=True)
    calendar_event_id = graphene.String()
    status = graphene.Field(BookingStatusEnumGraphene)
    start_time = graphene.DateTime(required=True)
    end_time = graphene.DateTime(required=True)
    study_id = graphene.ID(required=True)


class BookingUpdateInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    machine_code = graphene.String()
    calendar_event_id = graphene.String()
    status = graphene.Field(BookingStatusEnumGraphene)
    start_time = graphene.DateTime()
    end_time = graphene.DateTime()
