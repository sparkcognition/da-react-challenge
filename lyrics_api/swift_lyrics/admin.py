from django.contrib import admin

# Register your models here.
from swift_lyrics.models import Artist, Lyric, Song, Album

admin.site.register(Lyric)
admin.site.register(Song)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "first_year_active")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "artist", )
