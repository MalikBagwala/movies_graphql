from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import SystemUser
import graphene


class SystemUserType(DjangoObjectType):
    full_name = graphene.String()
    age = graphene.Int()

    class Meta:
        model = SystemUser
