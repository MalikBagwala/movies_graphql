import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
# Genre DB Model
from movies_graphql.moviedb.models import Actor
# Genre GraphQL Type
from movies_graphql.moviedb.actor.actortypes import ActorType


class ActorMutation(object):
    pass
