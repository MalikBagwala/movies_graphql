import graphene
from django.db.models import Avg, Count
from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import Movie, Rating


class MovieType(DjangoObjectType):
    rating = graphene.Float()
    total_votes = graphene.Int()

    @staticmethod
    def resolve_total_votes(parent, info):
        total_votes = Rating.objects.filter(
            movie_id=parent.id).aggregate(total=Count("rating"))
        return total_votes['total']

    @staticmethod
    def resolve_rating(parent, info):
        avg_rating = Rating.objects.filter(
            movie_id=parent.id).aggregate(rating=Avg("rating"))

        avg = avg_rating['rating']

        if avg is not None:
            return round(avg_rating['rating'], 1)
        else:
            return avg

    class Meta:
        model = Movie
