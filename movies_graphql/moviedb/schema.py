import graphene
from django.db.models import Q, Avg
from graphene_django.types import DjangoObjectType
import movies_graphql.moviedb.models as models

# Types


class GenreType(DjangoObjectType):
    class Meta:
        model = models.Genre


class ActorType(DjangoObjectType):
    full_name = graphene.String()
    age = graphene.Int()

    class Meta:
        model = models.Actor


class MovieType(DjangoObjectType):
    rating = graphene.Float()

    @staticmethod
    def resolve_rating(parent, info):
        avg_rating = models.Rating.objects.filter(
            movie_id=parent.id).aggregate(rating=Avg("rating"))
        return avg_rating['rating']

    class Meta:
        model = models.Movie


# Queries


class Query(graphene.ObjectType):
    all_genres = graphene.List(GenreType, search=graphene.String())
    all_movies = graphene.List(MovieType, search=graphene.String())
    genre = graphene.Field(GenreType, id=graphene.ID(), name=graphene.String())

    def resolve_all_genres(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(name__icontains=search))
            return models.Genre.objects.filter(filter)
        return models.Genre.objects.all()

    def resolve_all_movies(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(title__icontains=search))
            return models.Movie.objects.filter(filter)
        return models.Movie.objects.all()

    def resolve_genre(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return models.Genre.objects.get(pk=id)

        if name is not None:
            return models.Genre.objects.get(name__iexact=name)

        return None

# Mutations


class AddEditGenre(graphene.Mutation):
    genre = graphene.Field(GenreType)

    class Arguments:
        id = graphene.Int(required=False)
        name = graphene.String()

    def mutate(self, info, **arg):
        name = arg.get("name")
        id = arg.get("id")

        obj, created = models.Genre.objects.update_or_create(
            id=id,
            defaults={"name": name}
        )
        return AddEditGenre(genre=obj)


class Mutation(graphene.ObjectType):
    add_edit_genre = AddEditGenre.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
