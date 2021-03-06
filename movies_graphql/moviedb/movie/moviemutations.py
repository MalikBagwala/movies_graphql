import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
# Genre DB Model
from movies_graphql.moviedb.models import Movie
# Genre GraphQL Type
from movies_graphql.moviedb.movie.movietypes import MovieType


class AddEditMovie(graphene.Mutation):
    movie = graphene.Field(MovieType)

    class Arguments:
        id = graphene.ID(required=False)
        title = graphene.String()
        boxOffice = graphene.Float(required=False)
        budget = graphene.Float(required=False)
        releaseDate = graphene.Date(required=False)
        actors = graphene.List(graphene.ID)
        genres = graphene.List(graphene.ID)

    def mutate(self, info, **arg):
        id = arg.get("id")
        title = arg.get("title")
        boxOffice = arg.get("boxOffice")
        budget = arg.get("budget")
        releaseDate = arg.get("releaseDate")
        actors = arg.get("actors")
        genres = arg.get("genres")

        obj, created = Movie.objects.update_or_create(
            id=id,
            defaults={"title": title,
                      "release_date": releaseDate, "box_office": boxOffice, "budget": budget}
        )
        obj.actors.set(actors)
        obj.genres.set(genres)
        return AddEditMovie(movie=obj)


class DeleteMovies(graphene.Mutation):
    movies = graphene.List(graphene.ID)

    class Arguments:
        movies = graphene.List(graphene.ID)

    def mutate(self, info, movies):
        deletedMovies = Movie.objects.filter(pk__in=movies).delete()
        if deletedMovies[0] > 0:
            return DeleteMovies(movies=movies)
        else:
            return None


class MovieMutation(object):
    add_edit_movie = AddEditMovie.Field()
    delete_movies = DeleteMovies.Field()
