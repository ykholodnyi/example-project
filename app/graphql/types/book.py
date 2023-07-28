import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.models import Book, Genre


class BookType(SQLAlchemyObjectType):
    class Meta:
        model = Book
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection

    id = graphene.ID(required=True)

    def resolve_id(self, info):
        return self.id


class BookCreateInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    author_id = graphene.ID(required=True)


class BookUpdateInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    title = graphene.String()
    author = graphene.ID()
    genres = graphene.List(graphene.ID)


class GenreType(SQLAlchemyObjectType):
    class Meta:
        model = Genre
        interfaces = (graphene.relay.Node, )
        connection_class = graphene.Connection

    id = graphene.ID(required=True)

    def resolve_id(self, info):
        return self.id


class GenreCreateInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    books = graphene.List(graphene.ID)


class GenreUpdateInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    books = graphene.List(graphene.ID)
