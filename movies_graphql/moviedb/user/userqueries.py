import graphene
from django.db.models import Q
from movies_graphql.moviedb.models import SystemUser
from movies_graphql.moviedb.user.usertypes import SystemUserType, MyData
from graphql_jwt.decorators import login_required
# SystemUser Queries


class SystemUserQuery(object):
    me = graphene.Field(MyData)
    all_users = graphene.List(SystemUserType, search=graphene.String())
    user = graphene.Field(
        SystemUserType, id=graphene.ID(), name=graphene.String())

    def resolve_all_users(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(first_name__icontains=search)
                      | Q(last_name__icontains=search) | Q(number__icontains=search))
            return SystemUser.objects.filter(filter)
        return SystemUser.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return SystemUser.objects.get(pk=id)
        return None

    @login_required
    def resolve_me(self, info, **kwargs):
        return MyData(
            user=info.context.user,
        )
