from django.db import models


class Artist(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    instrument = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class RecordLabel(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    name = models.CharField(max_length=100, null=False, blank=False)
    release_date = models.DateField(null=False, blank=False)
    record_label = models.ForeignKey(RecordLabel, on_delete=models.CASCADE, related_name="albums")

    def __str__(self):
        return f"{self.name} by {self.artist}"


class Song(models.Model):
    artists = models.ManyToManyField(Artist, related_name="songs")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    name = models.CharField(max_length=100, null=False, blank=False)
    release_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name
