import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from movies_graphql.moviedb.models import Genre

# Types


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre

# Queries


class Query(graphene.ObjectType):
    all_genres = graphene.List(GenreType, search=graphene.String())
    genre = graphene.Field(GenreType, id=graphene.ID(), name=graphene.String())

    def resolve_all_genres(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(name__icontains=search))
            return Genre.objects.filter(filter)
        return Genre.objects.all()

    def resolve_genre(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Genre.objects.get(pk=id)

        if name is not None:
            return Genre.objects.get(name__iexact=name)

        return None

# Mutations


class AddEditGenre(graphene.Mutation):
    genre = graphene.Field(GenreType)

    class Arguments:
        id = graphene.ID(required=False)
        name = graphene.String()

    def mutate(self, info, **arg):
        name = arg.get("name")
        id = arg.get("id")

        obj, created = Genre.objects.update_or_create(
            id=id,
            defaults={"name": name}
        )
        return AddEditGenre(genre=obj)


class Mutation(graphene.ObjectType):
    add_edit_genre = AddEditGenre.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
