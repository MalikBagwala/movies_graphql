from datetime import datetime
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
# Abstract Classes


class Timestamp(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Updated At", auto_now=True
    )

    class Meta:
        abstract = True


class SystemUser(AbstractUser, Timestamp):
    number = models.CharField(
        max_length=15, verbose_name="Phone Number", unique=True, null=True
    )
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date_of_birth = models.DateField(
        verbose_name="Date Of Birth", null=True, blank=True)

    @property
    def age(self):
        if self.date_of_birth is not None:
            return int((datetime.now().date() - self.date_of_birth).days / 365.25)
        return None

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name
    pass


class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=True, blank=True, verbose_name="First Name")
    last_name = models.CharField(
        max_length=60, null=True, blank=True, verbose_name="Last Name")
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


class Movie(Timestamp):
    title = models.CharField(max_length=128, verbose_name="Movie Title")
    budget = models.FloatField(null=True, blank=True)
    box_office = models.FloatField("Box Office", null=True, blank=True)
    release_date = models.DateField("Release Date")
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return f'{self.title} - {self.release_date}'


class Rating(Timestamp):
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.movie} : {self.rating}'

    class Meta:
        unique_together = (("user", "movie"),)
