import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.graphql.mixins import IDTypeMixin
from app.models import Author, Biography


class AuthorType(SQLAlchemyObjectType, IDTypeMixin):
    class Meta:
        model = Author
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection


class AuthorCreateInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class AuthorUpdateInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    books = graphene.List(graphene.ID)


class BiographyType(SQLAlchemyObjectType, IDTypeMixin):
    class Meta:
        model = Biography
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection


class BiographyCreateInputType(graphene.InputObjectType):
    content = graphene.String(required=True)
    author_id = graphene.ID(required=True)


class BiographyUpdateInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    content = graphene.String()
    author_id = graphene.ID()
