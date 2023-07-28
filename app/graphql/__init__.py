import graphene

from app.graphql.queries import Query
from app.graphql.mutations import Mutation

graphql_schema = graphene.Schema(query=Query, mutation=Mutation)

