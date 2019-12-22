import graphene
from django.db.models import Q
from movies_graphql.moviedb.models import Rating
from movies_graphql.moviedb.rating.ratingtypes import RatingType

# Rating Queries


class RatingQuery(object):
    all_ratings = graphene.List(RatingType, search=graphene.String())
    rating = graphene.Field(
        RatingType, id=graphene.ID(), name=graphene.String())

    def resolve_all_ratings(self, info, **kwargs):
        search = kwargs.get("search")
        if search:
            filter = (Q(name__icontains=search))
            return Rating.objects.filter(filter)
        return Rating.objects.all()

    def resolve_rating(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Rating.objects.get(pk=id)
        return None
