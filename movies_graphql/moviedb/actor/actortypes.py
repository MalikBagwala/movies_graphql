import graphene
from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import Actor


class ActorType(DjangoObjectType):
    full_name = graphene.String()
    age = graphene.Int()

    class Meta:
        model = Actor
