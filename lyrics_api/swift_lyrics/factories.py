import factory

from swift_lyrics.models import Album, Artist, Lyric, Song


class ArtistFactory(factory.django.DjangoModelFactory):
    """
    Artist Factory for testing
    """

    name = factory.Faker("sentence", nb_words=6)
    first_year_active = factory.Faker("pyint", min_value=1960, max_value=2021)

    class Meta:
        model = Artist


class AlbumFactory(factory.django.DjangoModelFactory):
    """
    Album Factory for testing
    """

    artist = factory.SubFactory(ArtistFactory)
    name = factory.Faker("sentence", nb_words=6)
    year = factory.Faker("pyint", min_value=1960, max_value=2021)

    class Meta:
        model = Album


class SongFactory(factory.django.DjangoModelFactory):
    """
    Song Factory for testing
    """

    album = factory.SubFactory(AlbumFactory)
    name = factory.Faker("sentence", nb_words=6)

    class Meta:
        model = Song


class LyricFactory(factory.django.DjangoModelFactory):
    """
    Lyric Factory for testing
    """

    song = factory.SubFactory(SongFactory)
    text = factory.Faker("paragraph")

    class Meta:
        model = Lyric
