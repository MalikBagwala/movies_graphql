import graphene
from django.db.models import Q
from movies_graphql.moviedb.models import Actor
from movies_graphql.moviedb.actor.actortypes import ActorType

# Genre Queries


class ActorQuery(object):
    all_actors = graphene.List(ActorType, search=graphene.String())
    actor = graphene.Field(ActorType, id=graphene.ID())

    def resolve_all_actors(self, _, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(name__icontains=search))
            return Actor.objects.filter(filter)
        return Actor.objects.all()

    def resolve_actor(self, _, **kwargs):
        id = kwargs.get("id")

        return Actor.objects.get(pk=id)
