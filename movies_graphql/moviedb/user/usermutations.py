import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
# Genre DB Model
from movies_graphql.moviedb.models import SystemUser
# Genre GraphQL Type
from movies_graphql.moviedb.user.usertypes import SystemUserType

from graphql_jwt.decorators import token_auth
from graphql_jwt import JSONWebTokenMutation
import graphql_jwt


class Login(JSONWebTokenMutation):
    user = graphene.Field(SystemUserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class AddEditUser(graphene.Mutation):
    user = graphene.Field(SystemUserType)

    class Arguments:
        id = graphene.Int(required=False)
        username = graphene.String()
        password = graphene.String()
        firstName = graphene.String(required=False)
        lastName = graphene.String(required=False)
        dateOfBirth = graphene.Date(required=False)

    def mutate(self, info, **arg):
        id = arg.get("id")
        firstName = arg.get("firstName")
        lastName = arg.get("lastName")
        dateOfBirth = arg.get("dateOfBirth")
        username = arg.get("username")
        password = arg.get("password")
        obj, created = SystemUser.objects.update_or_create(
            id=id,
            defaults={"first_name": firstName,
                      "last_name": lastName, "date_of_birth": dateOfBirth, "username": username}
        )
        obj.set_password(password)
        obj.save()
        return AddEditUser(user=obj)


class UserMutation(object):
    login = Login.Field()
    add_edit_user = AddEditUser.Field()
