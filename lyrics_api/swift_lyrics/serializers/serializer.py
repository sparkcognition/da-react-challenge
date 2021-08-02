from drf_yasg import openapi
from rest_framework import serializers

from swift_lyrics.models import Lyric, Song, Album, Artist


class BaseArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['id', 'name', 'first_year_active']


class BaseAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['id', 'name']


class BaseSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ['id', 'name']


class LyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ['id', 'text', 'votes', 'upvotes', 'downvotes']
        read_only_fields = ['votes', 'upvotes', 'downvotes']


class ArtistDetailSerializer(BaseArtistSerializer):
    albums = BaseAlbumSerializer(many=True, read_only=True)

    class Meta(BaseArtistSerializer.Meta):
        fields = BaseArtistSerializer.Meta.fields + ['albums']


class AlbumDetailSerializer(BaseAlbumSerializer):
    songs = BaseSongSerializer(many=True, read_only=True)
    artist = BaseArtistSerializer()

    class Meta(BaseAlbumSerializer.Meta):
        fields = BaseAlbumSerializer.Meta.fields + ['songs', 'artist']


class SongSerializer(BaseSongSerializer):
    album = BaseAlbumSerializer()

    class Meta(BaseSongSerializer.Meta):
        fields = BaseSongSerializer.Meta.fields + ['album']


class SongDetailSerializer(SongSerializer):
    lyrics = LyricSerializer(many=True, read_only=True)

    class Meta(SongSerializer.Meta):
        fields = SongSerializer.Meta.fields + ['lyrics']


class LyricDetailSerializer(LyricSerializer):
    song = BaseSongSerializer(read_only=True)
    album = BaseAlbumSerializer(source='song.album', read_only=True)
    artist = BaseArtistSerializer(source='song.album.artist', read_only=True)

    def validate(self, data):
        song_id = self.initial_data.get('song', dict()).get('id', None)
        if song_id:
            # If song_id, then the album and song already exist, just fetch them from datastore
            song = Song.objects.get(id=song_id)
            data['song'] = song
        else:
            # If album_id, then album already exists - just fetch, then handle create/fetch song
            album_id = self.initial_data.get('album', dict()).get('id', None)

            song = self.initial_data.get('song', dict())
            song_name = song.get('name', None)

            album = None
            if album_id:
                album = Album.objects.get(id=album_id)
            else:
                album_name = self.initial_data.get('album', dict()).get('name', None)
                if album_name:
                    album = Album.objects.filter(name=album_name).first()
                    if album is None:
                        album = Album(name=album_name)
                        album.save()

            if song_name:
                song = Song.objects.filter(name=song_name).first()
                if song is None:
                    song = Song(name=song_name, album=album)
                    song.save()
                data['song'] = song

        return super().validate(data)

    def create(self, validated_data):
        lyric = Lyric(**validated_data)
        lyric.save()
        return lyric

    class Meta(LyricSerializer.Meta):
        fields = LyricSerializer.Meta.fields + ['song', 'album', 'artist']
