import logging

import graphene

from app.graphql.types.book import (
    BookType, BookCreateInputType, BookUpdateInputType,
    GenreType, GenreCreateInputType, GenreUpdateInputType
)

from app.models import Book, Genre
from app.graphql.mixins import CRUMixin

logger = logging.getLogger(__name__)


class CreateBook(graphene.Mutation, CRUMixin):
    class Arguments:
        book = graphene.Argument(BookCreateInputType, required=True)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, book, **kwargs):
        obj = Book(**book)
        obj = cls.add_object(obj=obj, session=info.context["request"].state.db)
        return CreateBook(book=obj)


class UpdateBook(graphene.Mutation, CRUMixin):
    class Arguments:
        book = graphene.Argument(BookUpdateInputType, required=True)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, book, **kwargs):
        session = info.context["request"].state.db
        obj = cls.get_object(obj_id=book.id, model=Book, session=session)
        obj = cls.update_object(obj=obj, data=book, session=session)
        return UpdateBook(book=obj)


class CreateGenre(graphene.Mutation, CRUMixin):
    class Arguments:
        genre = graphene.Argument(GenreCreateInputType, required=True)

    genre = graphene.Field(GenreType)

    @classmethod
    def mutate(cls, root, info, genre, **kwargs):
        obj = Genre(**genre)
        obj = cls.add_object(obj=obj, session=info.context["request"].state.db)
        return CreateGenre(genre=obj)


class UpdateGenre(graphene.Mutation, CRUMixin):
    class Arguments:
        genre = graphene.Argument(GenreUpdateInputType, required=True)

    genre = graphene.Field(GenreType)

    @classmethod
    def mutate(cls, root, info, genre, **kwargs):
        session = info.context["request"].state.db
        obj = cls.get_object(obj_id=genre.id, model=Genre, session=session)
        obj = cls.update_object(obj, genre, session=session)
        return UpdateGenre(genre=obj)
