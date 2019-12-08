import graphene
from django.db.models import Q
from movies_graphql.moviedb.models import Movie
from movies_graphql.moviedb.movie.movietypes import MovieType


class MovieQuery(object):
    all_movies = graphene.List(MovieType, search=graphene.String())

    def resolve_all_movies(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(title__icontains=search))
            return Movie.objects.filter(filter)
        return Movie.objects.order_by("-created_at")
