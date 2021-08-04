import random

from django.http import HttpResponse
from django.views import View
from django.db import models

from rest_framework import mixins, generics, filters, viewsets, response

from django_filters import rest_framework as django_filters

from swift_lyrics.filters import ArtistFilter, RandomLyricFilter
from swift_lyrics.models import Lyric, Album, Song, Artist
from swift_lyrics.serializers.serializer import (
    BaseArtistSerializer,
    AlbumDetailSerializer,
    AlbumCreationSerializer,
    ArtistDetailSerializer,
    SongDetailSerializer,
    SongSerializer,
    LyricDetailSerializer,
)


class HealthCheckView(View):
    """
    Checks if the site is alive.
    """

    def get(self, request, *args, **kwargs):
        """Basic Response"""

        return HttpResponse("ok")


class ArtistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Artist-related endpoints.
    """

    queryset = Artist.objects.all()
    serializer_class = BaseArtistSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ArtistFilter
    ordering_fields = ["first_year_active", "name"]

    def get_serializer_class(self):
        """
        Replaces default serializer according to endpoint
        """

        if self.action == "retrieve":
            return ArtistDetailSerializer
        return super().get_serializer_class()

class AlbumIndex(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    View for Album list retrieval and creation.
    """

    serializer_class = AlbumDetailSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        """Basic list retrieval"""

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Basic Album creation"""

        self.serializer_class = AlbumCreationSerializer
        return self.create(request, *args, **kwargs)


class AlbumDetail(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    View for Album retrieval and deletion.
    """

    serializer_class = AlbumDetailSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        """Basic retrieval"""

        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Basic deletion"""

        return self.destroy(request, *args, **kwargs)


class SongIndex(mixins.ListModelMixin, generics.GenericAPIView):
    """
    View for Song list retrieval.
    """

    serializer_class = SongSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        """Basic retrieval"""

        return self.list(request, *args, **kwargs)


class SongDetail(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    View for Song retrieval and deletion.
    """

    serializer_class = SongDetailSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        """Basic retrieval"""

        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Basic deletion"""

        return self.destroy(request, *args, **kwargs)


class UpvoteLyricDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    View for Song upvoting.
    """

    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Increase of votes and upvotes for matching query and return of instance
        """

        Lyric.objects.filter(**kwargs).update(
            votes=models.F("votes") + 1, upvotes=models.F("upvotes") + 1
        )
        return self.retrieve(request, *args, **kwargs)


class DownvoteLyricDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    View for Song downvoting.
    """

    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Increase of votes and downvotes for matching query and return of instance
        """

        Lyric.objects.filter(**kwargs).update(
            votes=models.F("votes") + 1, downvotes=models.F("downvotes") + 1
        )
        return self.retrieve(request, *args, **kwargs)


class RandomLyricDetail(generics.GenericAPIView):
    """
    View for random Song retrieval.
    """

    serializer_class = LyricDetailSerializer
    pagination_class = None
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = RandomLyricFilter

    def get_queryset(self):
        """Custom Queryset function"""

        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Obtains a random Lyric instance and returns as response
        """

        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return response.Response(dict())
        random_id = random.choice(queryset.values_list("id", flat=True))
        serializer = self.get_serializer(queryset.get(id=random_id))

        return response.Response(serializer.data)


class APIIndex(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = LyricDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["text", "song__name", "song__album__name"]
    ordering_fields = ["text", "song__name", "song__album__name"]

    def get_queryset(self):
        """Custom Queryset function"""

        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        """Basic list retrieval"""

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Basic Lyric creation"""

        return self.create(request, *args, **kwargs)


class APIDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        """Custom Queryset function"""

        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        """Basic retrieval"""

        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Basic deletion"""

        return self.destroy(request, *args, **kwargs)
