from django.contrib import admin
from .models import Song, SongRating
# Register your models here.
admin.site.register(Song)

admin.site.register(SongRating)