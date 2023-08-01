import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.graphql.mixins import IDTypeMixin
from app.models import Study


class StudyType(SQLAlchemyObjectType, IDTypeMixin):
    class Meta:
        model = Study
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection


class StudyCreateInputType(graphene.InputObjectType):
    patient = graphene.String(required=True)