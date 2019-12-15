from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import SystemUser


class SystemUserType(DjangoObjectType):
    class Meta:
        model = SystemUser
