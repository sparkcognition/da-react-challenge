from drf_yasg import openapi
from rest_framework import serializers

from swift_lyrics.models import Lyric, Song, Album, Artist


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['id', 'name', 'first_year_active']


class BaseAlbumSerializer(serializers.ModelSerializer):

    year = serializers.IntegerField(required=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'year']


# An specific serializer for create endpoint is needed for documentation purposes,
# since OpenAPI does not support writeOnly fields.
# See https://github.com/axnsan12/drf-yasg/issues/70
class AlbumWriteSerializer(BaseAlbumSerializer):

    artist_name = serializers.CharField(max_length=200, write_only=True)

    class Meta(BaseAlbumSerializer.Meta):
        fields = BaseAlbumSerializer.Meta.fields + ["artist_name"]

    def create(self, validated_data):
        artist_name = validated_data.pop("artist_name")
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        validated_data["artist"] = artist
        instance = Album.objects.create(**validated_data)
        return instance


class BaseSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ['id', 'name']


class LyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ['id', 'text', 'votes']


class AlbumDetailSerializer(BaseAlbumSerializer):
    songs = BaseSongSerializer(many=True, read_only=True)

    class Meta(BaseAlbumSerializer.Meta):
        fields = BaseAlbumSerializer.Meta.fields + ['songs']


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

    def validate(self, data):
        song_id = self.initial_data.get('song', dict()).get('id', None)
        album_id = self.initial_data.get('album', dict()).get('id', None)
        if not album_id:
            raise serializers.ValidationError("album.id is required")
        try:
            Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            raise serializers.ValidationError(
                f"There is not album with the id={album_id}. Try another one.")

        if song_id:
            # If song_id, then the album and song already exist, just fetch them from datastore
            song = Song.objects.get(id=song_id)
            data['song'] = song
        else:

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
        fields = LyricSerializer.Meta.fields + ['song', 'album']
