import graphene
from graphene import relay

from app.graphql.queries.book import BookQuery
from app.graphql.queries.author import AuthorQuery


class Query(
    graphene.ObjectType,
    BookQuery,
    AuthorQuery,
):
    node = relay.Node.Field()
