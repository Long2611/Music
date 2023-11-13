from django.db import models
from django_countries.fields import CountryField


#import settings
from django.conf import settings

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
#import validators
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Song(TimeStampedModel):

    # Below are fields from the spotify get track endpoint
    name = models.CharField("Name of Song", max_length=255)
    spotify_id = models.CharField("Spotify ID", max_length=255)
    album = models.CharField("Album", max_length=255)
    artist = models.CharField("Artist", max_length=255)
    release_date = models.DateField("Release Date")
    popularity = models.PositiveIntegerField("Popularity")
    duration_ms = models.PositiveIntegerField("Duration (ms)")
    explicit = models.BooleanField("Explicit")
    image_url = models.URLField("Image URL")
    genres = models.CharField("Genres", max_length=255, blank=True, null=True)

    #average rating method to get the average rating of a song
    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.songrating_set.all())
        return np.mean(all_ratings)

    
# Song rating model
class SongRating(TimeStampedModel):
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )

    Song = models.ForeignKey(
        Song,
        null=True,
        on_delete=models.SET_NULL,
    )