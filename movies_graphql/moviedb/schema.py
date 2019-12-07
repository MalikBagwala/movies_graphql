import graphene
from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import Genre


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre


class Query(graphene.ObjectType):
    all_genres = graphene.List(GenreType)
    genre = graphene.Field(GenreType, id=graphene.ID(), name=graphene.String())

    def resolve_all_genres(self, info, **kwargs):
        return Genre.objects.all()

    def resolve_genre(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Genre.objects.get(pk=id)

        if name is not None:
            return Genre.objects.get(name__iexact=name)

        return None


schema = graphene.Schema(query=Query)
