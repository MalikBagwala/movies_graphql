import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
import movies_graphql.moviedb.models as models

# Queries
from movies_graphql.moviedb.genre.genrequeries import GenreQuery
from movies_graphql.moviedb.movie.moviequeries import MovieQuery
from movies_graphql.moviedb.actor.actorqueries import ActorQuery
from movies_graphql.moviedb.user.userqueries import SystemUserQuery
from movies_graphql.moviedb.rating.ratingqueries import RatingQuery
# Mutations
from movies_graphql.moviedb.genre.genremutations import GenreMutation
from movies_graphql.moviedb.rating.ratingmutations import RatingMutation
from movies_graphql.moviedb.actor.actormutations import ActorMutation
from movies_graphql.moviedb.movie.moviemutations import MovieMutation
from movies_graphql.moviedb.user.usermutations import UserMutation

# graphql jwt
import graphql_jwt


class Query(GenreQuery, MovieQuery, ActorQuery, SystemUserQuery, RatingQuery, graphene.ObjectType):
    pass


class Mutation(GenreMutation, RatingMutation, ActorMutation, MovieMutation, UserMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
