from rest_framework import mixins, filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import HttpResponse
from django.views import View
from drf_yasg.utils import no_body, swagger_auto_schema
# Create your views here.
from swift_lyrics.models import Lyric, Album, Song
from swift_lyrics.serializers.serializer import BaseAlbumSerializer, \
    AlbumDetailSerializer, AlbumWriteSerializer, SongDetailSerializer, \
    SongSerializer, LyricDetailSerializer


class HealthCheckView(View):
    """
    Checks to see if the site is healthy.
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")


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
