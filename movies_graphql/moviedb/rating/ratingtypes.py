from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import Rating


class RatingType(DjangoObjectType):
    class Meta:
        model = Rating
