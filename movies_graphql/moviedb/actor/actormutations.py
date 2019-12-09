import graphene
from django.db.models import Q, Avg, Count
from graphene_django.types import DjangoObjectType
# Genre DB Model
from movies_graphql.moviedb.models import Actor
# Genre GraphQL Type
from movies_graphql.moviedb.actor.actortypes import ActorType


class AddEditActor(graphene.Mutation):
    actor = graphene.Field(ActorType)

    class Arguments:
        id = graphene.Int(required=False)
        firstName = graphene.String()
        lastName = graphene.String()
        dateOfBirth = graphene.Date()

    def mutate(self, info, **arg):
        id = arg.get("id")
        firstName = arg.get("firstName")
        lastName = arg.get("lastName")
        dateOfBirth = arg.get("dateOfBirth")

        obj, created = Actor.objects.update_or_create(
            id=id,
            defaults={"first_name": firstName,
                      "last_name": lastName, "date_of_birth": dateOfBirth}
        )
        return AddEditActor(actor=obj)


class DeleteActors(graphene.Mutation):
    actors = graphene.List(graphene.ID)

    class Arguments:
        actors = graphene.List(graphene.ID)

    def mutate(self, info, actors):
        deletedActors = Actor.objects.filter(pk__in=actors).delete()
        if deletedActors[0] > 0:
            return DeleteActors(actors=actors)
        else:
            return None


class ActorMutation(object):
    add_edit_actor = AddEditActor.Field()
    delete_actors = DeleteActors.Field()
