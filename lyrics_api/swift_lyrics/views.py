from rest_framework import mixins, filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import HttpResponse, Http404
from django.views import View
from django_filters import rest_framework as dj_filters
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema

from swift_lyrics.models import Artist, Lyric, Album, Song
from swift_lyrics.serializers.serializer import BaseAlbumSerializer, \
    AlbumDetailSerializer, AlbumWriteSerializer, SongDetailSerializer, \
    SongSerializer, LyricDetailSerializer, ArtistSerializer, ArtistDetailSerializer


class HealthCheckView(View):
    """
    Checks to see if the site is healthy.
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")


class ArtistFilter(dj_filters.FilterSet):
    min_first_year = dj_filters.NumberFilter(field_name="first_year_active", lookup_expr='gte')
    max_first_year = dj_filters.NumberFilter(field_name="first_year_active", lookup_expr='lte')

    class Meta:
        model = Artist
        fields = ['min_first_year', 'max_first_year']


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = [filters.OrderingFilter, dj_filters.DjangoFilterBackend]
    filterset_class = ArtistFilter
    ordering_fields = ['name', 'first_year_active']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        else:
            return ArtistSerializer


class AlbumViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AlbumDetailSerializer
        elif self.action == "create":
            return AlbumWriteSerializer
        else:
            return BaseAlbumSerializer


class SongViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Song.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SongDetailSerializer
        else:
            return SongSerializer


class LyricViewSet(viewsets.ModelViewSet):
    queryset = Lyric.objects.all()
    serializer_class = LyricDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'song__name', 'song__album__name']
    ordering_fields = ['text', 'song__name', 'song__album__name']

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def vote_up(self, request, pk=None):
        lyric = self.get_object()
        lyric.vote(request.user, +1)
        serializer = self.get_serializer(lyric)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def vote_down(self, request, pk=None):
        lyric = self.get_object()
        lyric.vote(request.user, -1)
        serializer = self.get_serializer(lyric)
        return Response(serializer.data)

    # TODO: find a way to remove the auto-generated parameters (search, ordering, page, size)
    @swagger_auto_schema(operation_description="Return a random lyric", manual_parameters=[
        openapi.Parameter('artist', in_=openapi.IN_QUERY, description='filter by artist name', type=openapi.TYPE_STRING),
    ])
    @action(detail=False, methods=["get"])
    def shuffle(self, request, pk=None):
        artist_name = request.query_params.get('artist')
        qs_lyrics = Lyric.objects
        if artist_name:
            qs_lyrics = qs_lyrics.filter(song__album__artist__name=artist_name)
        lyric = qs_lyrics.order_by('?').first()
        if not lyric:
            raise Http404
        serializer = self.get_serializer(lyric)
        return Response(serializer.data)
