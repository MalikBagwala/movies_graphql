import graphene
from movies_graphql.moviedb.models import Rating
from movies_graphql.moviedb.rating.ratingtypes import RatingType


class AddEditRating(graphene.Mutation):
    rating = graphene.Field(RatingType)

    class Arguments:
        movie = graphene.ID()
        user = graphene.ID()
        rating = graphene.Float()

    def mutate(self, info, **arg):
        user = arg.get("user")
        movie = arg.get("movie")
        rating = arg.get("rating")
        obj, created = Rating.objects.update_or_create(
            user_id=user,
            movie_id=movie,
            defaults={"rating": rating}
        )
        return AddEditRating(rating=obj)


class RatingMutation(object):
    add_edit_rating = AddEditRating.Field()
