import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
import movies_graphql.moviedb.models as models

# Queries
from movies_graphql.moviedb.genre.genrequeries import GenreQuery
from movies_graphql.moviedb.movie.moviequeries import MovieQuery
from movies_graphql.moviedb.actor.actorqueries import ActorQuery

# Mutations
from movies_graphql.moviedb.genre.genremutations import GenreMutation
from movies_graphql.moviedb.rating.ratingmutations import RatingMutation
from movies_graphql.moviedb.actor.actormutations import ActorMutation
from movies_graphql.moviedb.movie.moviemutations import MovieMutation
# Types


class UserType(DjangoObjectType):
    age = graphene.Int()

    class Meta:
        model = models.User


# Queries
class Query(GenreQuery, MovieQuery, ActorQuery, graphene.ObjectType):
    all_users = graphene.List(UserType, search=graphene.String())

    def resolve_all_users(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(first_name__icontains=search)
                      | Q(last_name__icontains=search) | Q(number__icontains=search))
            return models.User.objects.filter(filter)
        return models.User.objects.all()


class Mutation(GenreMutation, RatingMutation, ActorMutation, MovieMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
