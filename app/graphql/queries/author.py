import graphene
from sqlalchemy.orm import joinedload

from app.graphql.mixins import CRUMixin
from app.graphql.types.author import AuthorType, BiographyType
from app.models import Author, Biography, Book
from app.models.base import db_session


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
        return db_session.query(Author).options(
            joinedload(Author.books).joinedload(Book.genres),
            joinedload(Author.biography)
        ).all()

    @classmethod
    def resolve_biography(cls, _, info, biography_id):
        return cls.get_object(obj_id=biography_id, model=Biography)

    @classmethod
    def resolve_biographies(cls, _, info):
        return db_session.query(Biography).options(
            subq(Biography.author)
        ).all()
