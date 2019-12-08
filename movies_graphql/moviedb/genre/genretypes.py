from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import Genre

# All Genre Types


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
