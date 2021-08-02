from django.db import models


class Album(models.Model):
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=True,
        help_text="Album name - can alternatively use 'id' field set to id of existing album when creating new lyrics")

    objects = models.Manager()


class Song(models.Model):
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=True,
        help_text="Song name - can alternatively use 'id' field set to id of existing song when creating new lyrics")

    album = models.ForeignKey(
        Album,
        related_name='songs',
        null=True,
        on_delete=models.CASCADE,
        help_text="Album")

    objects = models.Manager()


class Lyric(models.Model):
    text = models.TextField(
        blank=False,
        db_index=True,
        help_text="Lyrics from a song/album")

    song = models.ForeignKey(
        Song,
        related_name='lyrics',
        null=True,
        on_delete=models.CASCADE,
        help_text="Song")

    votes = models.IntegerField(
        default=0
    )
    upvotes = models.IntegerField(
        default=0
    )
    downvotes = models.IntegerField(
        default=0
    )

    objects = models.Manager()
