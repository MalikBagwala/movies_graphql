from django.contrib import admin
import movies_graphql.moviedb.models as models
# Register your models here.

admin.site.register(models.Genre)
admin.site.register(models.Actor)
admin.site.register(models.Rating)
admin.site.register(models.User)
admin.site.register(models.Movie)