import graphene
from sqlalchemy.orm import joinedload, subqueryload

from app.graphql.mixins import CRUMixin
from app.graphql.types.book import BookType, GenreType
from app.models import Book, Genre
from app.models.base import db_session


class BookQuery(CRUMixin):
    book = graphene.Field(
        BookType,
        book_id=graphene.ID())

    books = graphene.List(BookType)

    genre = graphene.Field(
        GenreType,
        genre_id=graphene.ID())

    genres = graphene.List(GenreType)

    @classmethod
    def resolve_book(cls, _, info, book_id):
        return cls.get_object(obj_id=book_id, model=Book)

    @classmethod
    def resolve_books(cls, _, info):
        return db_session.query(Book).options(
            subqueryload(Book.genres),
            joinedload(Book.author),
        ).all()

    @classmethod
    def resolve_genre(cls, _, info, genre_id):
        return cls.get_object(obj_id=genre_id, model=Genre)

    @classmethod
    def resolve_genres(cls, _, info):
        return db_session.query(Genre).options(
            subqueryload(Genre.books),
        ).all()
