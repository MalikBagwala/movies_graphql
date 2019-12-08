import graphene
from django.db.models import Q
from movies_graphql.moviedb.models import Genre
from movies_graphql.moviedb.genre.genretypes import GenreType

# Genre Queries


class GenreQuery(object):
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
