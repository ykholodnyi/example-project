import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.models import Genre, Biography


class GenreType(SQLAlchemyObjectType):
    class Meta:
        model = Genre
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection


class BiographyType(SQLAlchemyObjectType):
    class Meta:
        model = Biography
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection
