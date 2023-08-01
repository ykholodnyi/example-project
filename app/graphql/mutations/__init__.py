import graphene

from app.graphql.mutations.book import CreateBook, UpdateBook, CreateGenre, UpdateGenre
from app.graphql.mutations.author import CreateAuthor, UpdateAuthor
from app.graphql.mutations.study import CreateStudy
from app.graphql.mutations.booking import CreateBooking, UpdateBooking


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()

    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()

    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()

    create_study = CreateStudy.Field()

    create_booking = CreateBooking.Field()
    update_booking = UpdateBooking.Field()
