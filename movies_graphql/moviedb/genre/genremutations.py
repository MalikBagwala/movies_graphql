import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
# Genre DB Model
from movies_graphql.moviedb.models import Genre
# Genre GraphQL Type
from movies_graphql.moviedb.genre.genretypes import GenreType


class AddEditGenre(graphene.Mutation):
    genre = graphene.Field(GenreType)

    class Arguments:
        id = graphene.Int(required=False)
        name = graphene.String()

    def mutate(self, info, **arg):
        name = arg.get("name")
        id = arg.get("id")

        obj, created = Genre.objects.update_or_create(
            id=id,
            defaults={"name": name}
        )
        return AddEditGenre(genre=obj)


class GenreMutation(object):
    add_edit_genre = AddEditGenre.Field()
