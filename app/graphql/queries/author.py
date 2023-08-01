import graphene
from sqlalchemy import subquery
from sqlalchemy.orm import joinedload

from app.graphql.mixins import CRUMixin
from app.graphql.types.author import AuthorType, BiographyType
from app.models import Author, Biography, Book


class AuthorQuery(CRUMixin):
    author = graphene.Field(
        AuthorType,
        author_id=graphene.ID())

    authors = graphene.List(AuthorType)

    biography = graphene.Field(
        BiographyType,
        biography_id=graphene.ID())

    biographies = graphene.List(BiographyType)

    @classmethod
    def resolve_author(cls, _, info, author_id):
        return cls.get_object(obj_id=author_id, model=Author)

    @classmethod
    def resolve_authors(cls, _, info):
        return info.context["request"].state.db.query(Author).options(
            joinedload(Author.books).joinedload(Book.genres),
            joinedload(Author.biography)
        ).all()

    @classmethod
    def resolve_biography(cls, _, info, biography_id):
        return cls.get_object(obj_id=biography_id, model=Biography, session=info.context["request"].state.db)

    @classmethod
    def resolve_biographies(cls, _, info):
        return info.context["request"].state.db.query(Biography).options(
            subquery(Biography.author)
        ).all()
