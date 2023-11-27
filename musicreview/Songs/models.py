from django.db import models
from django_countries.fields import CountryField


#import settings
from django.conf import settings

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
#import validators
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.db.models import Avg

# Create your models here.
class Song(TimeStampedModel):
    spotify_song_id = models.CharField(max_length=255, default='')

    def average_rating(self):
        return self.songrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    
# Song rating model
class SongRating(TimeStampedModel):
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)

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