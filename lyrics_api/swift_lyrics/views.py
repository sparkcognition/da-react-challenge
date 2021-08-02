from rest_framework import mixins, generics, filters, status
from rest_framework.response import Response

from django.http import HttpResponse
from django.views import View
from django.db import models
# Create your views here.
from swift_lyrics.models import Lyric, Album, Song, Artist
from swift_lyrics.serializers.serializer import BaseAlbumSerializer, BaseArtistSerializer, \
    AlbumDetailSerializer, AlbumCreationSerializer, ArtistDetailSerializer, \
    SongDetailSerializer, SongSerializer, LyricDetailSerializer


class HealthCheckView(View):
    """
    Checks to see if the site is healthy.
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")


class ArtistIndex(mixins.ListModelMixin,
                    generics.GenericAPIView):
    serializer_class = BaseArtistSerializer

    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ArtistDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):

    serializer_class = ArtistDetailSerializer

    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class AlbumIndex(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                 generics.GenericAPIView):
    serializer_class = BaseAlbumSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = AlbumCreationSerializer
        return self.create(request, *args, **kwargs)

class AlbumDetail(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = AlbumDetailSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SongIndex(mixins.ListModelMixin,
                 generics.GenericAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SongDetail(mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = SongDetailSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UpvoteLyricDetail(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        Lyric.objects.filter(**kwargs).update(
            votes=models.F('votes')+1, upvotes=models.F('upvotes')+1
        )
        return self.retrieve(request, *args, **kwargs)

class DownvoteLyricDetail(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        Lyric.objects.filter(**kwargs).update(
            votes=models.F('votes')+1, downvotes=models.F('downvotes')+1
        )
        return self.retrieve(request, *args, **kwargs)

class APIIndex(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    serializer_class = LyricDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'song__name', 'song__album__name']
    ordering_fields = ['text', 'song__name', 'song__album__name']


    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class APIDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    serializer_class = LyricDetailSerializer

    def get_queryset(self):
        return Lyric.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
