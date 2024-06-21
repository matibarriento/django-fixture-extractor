from django.contrib import admin
from .models import Artist, RecordLabel, Album, Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'instrument')
    search_fields = ('first_name', 'last_name', 'instrument')


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date', 'record_label')
    search_fields = ('name', 'artist__first_name', 'artist__last_name', 'record_label__name')
    list_filter = ('release_date', 'record_label')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'album', 'release_date')
    search_fields = ('name', 'album__name', 'artists__first_name', 'artists__last_name')
    list_filter = ('release_date', 'album')
