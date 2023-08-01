import graphene
from graphene import relay

from app.graphql.queries.book import BookQuery
from app.graphql.queries.author import AuthorQuery
from app.graphql.queries.booking import BookingQuery
from app.graphql.queries.study import StudyQuery


class Query(
    graphene.ObjectType,
    BookQuery,
    AuthorQuery,
    BookingQuery,
    StudyQuery,
):
    node = relay.Node.Field()
