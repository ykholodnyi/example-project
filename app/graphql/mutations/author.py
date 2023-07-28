import logging

import graphene

from app.graphql.types.author import (
    AuthorType, AuthorCreateInputType, AuthorUpdateInputType
)
from app.models import Author
from app.graphql.mixins import CRUMixin

logger = logging.getLogger(__name__)


class CreateAuthor(graphene.Mutation, CRUMixin):
    class Arguments:
        author = graphene.Argument(AuthorCreateInputType, required=True)

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, author, **kwargs):
        obj = Author(**author)
        obj = cls.add_object(obj=obj)
        return CreateAuthor(author=obj)


class UpdateAuthor(graphene.Mutation, CRUMixin):
    class Arguments:
        author = graphene.Argument(AuthorUpdateInputType, required=True)

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, author, **kwargs):
        obj = cls.get_object(obj_id=author.id, model=Author)
        obj = cls.update_object(obj, author)
        return UpdateAuthor(author=obj)
