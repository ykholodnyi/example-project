import graphene

from app.graphql.mutations.book import CreateBook, UpdateBook, CreateGenre, UpdateGenre
from app.graphql.mutations.author import CreateAuthor, UpdateAuthor


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()

    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()

    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
