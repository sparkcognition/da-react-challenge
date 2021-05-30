from django.contrib import admin

# Register your models here.
from swift_lyrics.models import Artist, Lyric, Song, Album


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "first_year_active", )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "artist", )


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("name", "album", )


@admin.register(Lyric)
class LyricAdmin(admin.ModelAdmin):
    list_display = ("text", "song", "votes", )
