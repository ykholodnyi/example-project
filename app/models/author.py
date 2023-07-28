from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    books = relationship('Book', back_populates='author', lazy='select')
    biography = relationship('Biography', uselist=False, back_populates='author')


class Biography(Base):
    __tablename__ = 'biographies'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='biography', lazy='joined')
