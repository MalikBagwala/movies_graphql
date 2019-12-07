from datetime import datetime
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Abstract Classes

class Timestamp(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Updated At", auto_now=True
    )

    class Meta:
        abstract = True


class Person(models.Model):
    first_name = models.CharField(max_length=60, verbose_name="First Name")
    last_name = models.CharField(max_length=60, verbose_name="Last Name")
    date_of_birth = models.DateField(
        verbose_name="Date Of Birth", null=True, blank=True)

    @property
    def age(self):
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        abstract = True


# Core Models

class Genre(Timestamp):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Actor(Person):
    pass


"""
The main Class For Movie Model
"""


class Movie(Timestamp):
    title = models.CharField(max_length=128, verbose_name="Movie Title")
    budget = models.FloatField()
    box_office = models.FloatField("Box Office")
    release_date = models.DateField("Release Date")
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title


class User(Person, Timestamp):
    uuid = models.UUIDField(
        "Universally Unique Identifier", unique=True, editable=False, default=uuid.uuid4
    )
    number = models.CharField(
        max_length=12, verbose_name="Phone Number", unique=True, null=True
    )
    email = models.CharField(max_length=50, unique=True, null=True)


class Rating(Timestamp):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.movie_id} : {self.rating}'

    class Meta:
        unique_together = (("user_id", "movie_id"),)
