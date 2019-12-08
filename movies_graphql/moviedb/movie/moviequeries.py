import graphene
from django.db.models import Q
from movies_graphql.moviedb.models import Movie
from movies_graphql.moviedb.movie.movietypes import MovieType


class MovieQuery(object):
    all_movies = graphene.List(MovieType, search=graphene.String())
    movie = graphene.Field(MovieType, id=graphene.ID())

    def resolve_all_movies(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(title__icontains=search))
            return Movie.objects.filter(filter)
        return Movie.objects.order_by("-created_at")

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Movie.objects.get(pk=id)

        return None
