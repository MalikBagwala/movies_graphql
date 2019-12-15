from django.contrib import admin
import movies_graphql.moviedb.models as models
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(models.SystemUser, UserAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Actor)
admin.site.register(models.Rating)
admin.site.register(models.Movie)
