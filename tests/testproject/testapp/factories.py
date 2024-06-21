from datetime import date

import factory.fuzzy
from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory
from faker import Factory

from tests.testproject.testapp.models import Artist, Album, RecordLabel, Song

faker = Factory.create()


class ArtistFactory(DjangoModelFactory):
    class Meta:
        model = Artist

    first_name = factory.fuzzy.FuzzyText(length=50)
    last_name = factory.fuzzy.FuzzyText(length=50)
    instrument = factory.fuzzy.FuzzyText(length=100)


class RecordLabelFactory(DjangoModelFactory):
    class Meta:
        model = RecordLabel

    name = factory.fuzzy.FuzzyText(length=50)


class AlbumFactory(DjangoModelFactory):
    class Meta:
        model = Album

    artist = SubFactory(ArtistFactory)
    name = factory.fuzzy.FuzzyText(length=50)
    release_date = factory.fuzzy.FuzzyDate(start_date=date(2019, 8, 3))
    record_label = SubFactory(RecordLabelFactory)


class SongFactory(DjangoModelFactory):
    class Meta:
        model = Song

    album = SubFactory(AlbumFactory)
    release_date = factory.fuzzy.FuzzyDate(start_date=date(2019, 8, 3))

    @post_generation
    def artists(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of artists were passed in, use them
            for artist in extracted:
                self.artists.add(artist)
