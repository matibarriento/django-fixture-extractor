from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE, related_name="albums")
    name = models.CharField(max_length=100, null=False, blank=False)
    release_date = models.DateField(null=False, blank=False)


class Song(models.Model):
    artists = models.ManyToManyField(Musician, related_name="songs")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    name = models.CharField(max_length=100, null=False, blank=False)
    release_date = models.DateField(null=False, blank=False)
