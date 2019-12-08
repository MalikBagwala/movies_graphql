import graphene
from django.db.models import Q, Avg, Count
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
    total_votes = graphene.Int()

    @staticmethod
    def resolve_total_votes(parent, info):
        total_votes = models.Rating.objects.filter(
            movie_id=parent.id).aggregate(total=Count("rating"))
        return total_votes['total']

    @staticmethod
    def resolve_rating(parent, info):
        avg_rating = models.Rating.objects.filter(
            movie_id=parent.id).aggregate(rating=Avg("rating"))

        avg = avg_rating['rating']

        if avg is not None:
            return round(avg_rating['rating'], 1)
        else:
            return avg

    class Meta:
        model = models.Movie


class RatingType(DjangoObjectType):
    class Meta:
        model = models.Rating


class UserType(DjangoObjectType):
    age = graphene.Int()

    class Meta:
        model = models.User


# Queries
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType, search=graphene.String())
    all_genres = graphene.List(GenreType, search=graphene.String())
    all_movies = graphene.List(MovieType, search=graphene.String())
    genre = graphene.Field(GenreType, id=graphene.ID(), name=graphene.String())

    def resolve_all_genres(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(name__icontains=search))
            return models.Genre.objects.filter(filter)
        return models.Genre.objects.all()

    def resolve_all_users(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(first_name__icontains=search)
                      | Q(last_name__icontains=search) | Q(number__icontains=search))
            return models.User.objects.filter(filter)
        return models.User.objects.all()

    def resolve_all_movies(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(title__icontains=search))
            return models.Movie.objects.filter(filter)
        return models.Movie.objects.order_by("-created_at")

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


class AddEditRating(graphene.Mutation):
    rating = graphene.Field(RatingType)

    class Arguments:
        movie = graphene.ID()
        user = graphene.ID()
        rating = graphene.Float()

    def mutate(self, info, **arg):
        user = arg.get("user")
        movie = arg.get("movie")
        rating = arg.get("rating")
        obj, created = models.Rating.objects.update_or_create(
            user_id=user,
            movie_id=movie,
            defaults={"rating": rating}
        )
        return AddEditRating(rating=obj)


class Mutation(graphene.ObjectType):
    add_edit_genre = AddEditGenre.Field()
    add_edit_rating = AddEditRating.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
