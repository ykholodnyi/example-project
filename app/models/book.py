from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.models.base import Base

# Many-to-Many Relationship
book_genre_association = Table(
    'book_genre_association',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='books', lazy='joined')
    genres = relationship('Genre', secondary=book_genre_association, back_populates='books', lazy='subquery')


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    books = relationship('Book', secondary=book_genre_association, back_populates='genres', lazy='subquery')
