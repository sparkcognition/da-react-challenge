from django.urls import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APITestCase

from faker import Faker

from swift_lyrics.models import Album, Artist, Lyric, Song
from swift_lyrics.factories import (
    AlbumFactory,
    ArtistFactory,
    LyricFactory,
    SongFactory,
)


class HealthCheckTest(APITestCase):
    """
    Tests HealthCheck endpoint
    """

    def test_01_healthcheck(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, HTTP_200_OK)


class AlbumViewTest(APITestCase):
    """
    Tests Album endpoints
    """

    def album_index(self):
        """
        Gets album index endpoint
        """

        return reverse("album_index")

    def album_detail(self, pk):
        """
        Gets album detail endpoint
        """

        return reverse("album_detail", kwargs={"pk": pk})

    def test_01_retrieve_all_albums(self):
        """
        Tests retrieval of all albums
        """

        response = self.client.get(self.album_index() + f"?size=100")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Album.objects.count())

    def test_02_retrieve_album(self):
        """
        Tests retrieval of a single album instance
        """

        album = AlbumFactory()
        response = self.client.get(self.album_detail(album.id))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["id"], album.id)
        self.assertEqual(response.data["year"], album.year)
        self.assertEqual(response.data["name"], album.name)

    def test_03_create_album(self):
        """
        Tests album creation
        """

        # First album includes a new artist as a dict
        first_album_name = "The awesome album"
        first_album_year = 2011
        album_artist = "Mouse Rat"
        body = dict(
            name=first_album_name,
            year=first_album_year,
            artist=dict(
                name=album_artist,
                first_year_active=2008,
            ),
        )
        response = self.client.post(self.album_index(), data=body, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["name"], first_album_name)
        self.assertEqual(response.data["year"], first_album_year)
        self.assertEqual(response.data["artist"]["name"], album_artist)
        album_artist_id = response.data["artist"]["id"]

        # Second album includes an existing artists,
        # identified by its neame
        second_album_name = "The awesome follow-up album"
        second_album_year = 2013
        body = dict(
            name=second_album_name,
            year=second_album_year,
            artist=dict(
                name=album_artist,
            ),
        )
        response = self.client.post(self.album_index(), data=body, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["name"], second_album_name)
        self.assertEqual(response.data["year"], second_album_year)
        self.assertEqual(response.data["artist"]["name"], album_artist)

        # Third album includes an artist id
        third_album_name = "The last album"
        third_album_year = 2015
        body = dict(
            name=third_album_name,
            year=third_album_year,
            artist=album_artist_id,
        )
        response = self.client.post(self.album_index(), data=body, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["name"], third_album_name)
        self.assertEqual(response.data["year"], third_album_year)
        self.assertEqual(response.data["artist"]["name"], album_artist)

    def test_04_create_album_error(self):
        """
        Tests errors in album creation
        """

        # Tests album creation with no information in data
        response = self.client.post(self.album_index(), data=dict(), format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Tests album creation with no artist data
        no_artist_dict = dict(name="Some artist", year=2013, artist=dict())
        response = self.client.post(
            self.album_index(), data=no_artist_dict, format="json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Tests album creation with incomplete artist data
        no_year_in_artist_dict = dict(
            name="Some artist", year=2013, artist=dict(name="Unknown artist")
        )
        response = self.client.post(
            self.album_index(), data=no_year_in_artist_dict, format="json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_05_delete_album(self):
        """
        Tests album deletion
        """

        album = Album.objects.first()
        response = self.client.delete(self.album_detail(album.id))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(Album.DoesNotExist):
            Album.objects.get(id=album.id)


class ArtistViewTest(APITestCase):
    """
    Tests Artist endpoints
    """

    def setUp(self):
        """
        Sets up Faker instance to be used on dummy word generation
        """

        Faker.seed()
        self.fake = Faker()
        super().setUp()

    def test_01_retrieve_artists(self):
        """
        Tests retrieval of all Artists and its filters
        """

        # Tests all artists retrieval
        url = reverse("artist-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Artist.objects.count())

        # Tests artists with lower than first_year_active filter
        artist = Artist.objects.first()
        url = (
            reverse("artist-list")
            + f"?first_year_active__lt={artist.first_year_active}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]),
            Artist.objects.filter(
                first_year_active__lt=artist.first_year_active
            ).count(),
        )

        # Tests artists with greater than first_year_active filter
        url = (
            reverse("artist-list")
            + f"?first_year_active__gt={artist.first_year_active}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]),
            Artist.objects.filter(
                first_year_active__gt=artist.first_year_active
            ).count(),
        )
        url = reverse("artist-list") + f"?name={artist.name}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_02_retrieve_single_artist(self):
        """
        Tests retrieval of a single artist
        """

        artist = ArtistFactory()
        url = reverse("artist-detail", kwargs=dict(pk=artist.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["id"], artist.id),
        self.assertEqual(response.data["name"], artist.name)
        self.assertEqual(response.data["first_year_active"], artist.first_year_active)

    def test_03_create_single_artist(self):
        """
        Tests artist creation
        """

        artist_name = self.fake.sentence(nb_words=6)
        artist_year = 2011
        artist_dict = dict(
            name=artist_name,
            first_year_active=artist_year,
        )
        url = reverse("artist-list")
        response = self.client.post(url, data=artist_dict, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["name"], artist_name)
        self.assertEqual(response.data["first_year_active"], artist_year)

    def test_04_update_single_artist(self):
        """
        Tests artist update
        """

        artist = Artist.objects.first()
        artist_name = self.fake.sentence(nb_words=6)
        artist_dict = dict(name=artist_name)
        url = reverse("artist-detail", kwargs=dict(pk=artist.id))
        response = self.client.patch(url, data=artist_dict, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["name"], artist_name)

    def test_05_delete_artist(self):
        """
        Tests artist deletion
        """

        artist = Artist.objects.first()
        url = reverse("artist-detail", kwargs=dict(pk=artist.id))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(Artist.DoesNotExist):
            Artist.objects.get(id=artist.id)


class SongViewTest(APITestCase):
    """
    Tests Song endpoints
    """

    def test_01_retrieve_all_songs(self):
        """
        Tests retrieval of all songs
        """

        response = self.client.get(reverse("song_index") + f"?size=100")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Song.objects.count())

    def test_02_retrieve_song(self):
        """
        Tests retrieval of a single song
        """

        song = SongFactory()
        response = self.client.get(reverse("song_detail", kwargs=dict(pk=song.id)))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["id"], song.id)
        self.assertEqual(response.data["name"], song.name)
        self.assertEqual(response.data["album"]["id"], song.album.id)
        self.assertEqual(response.data["album"]["artist"]["id"], song.album.artist.id)

    def test_03_delete_song(self):
        """
        Tests song deletion
        """

        song = SongFactory()
        response = self.client.delete(reverse("song_detail", kwargs=dict(pk=song.id)))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(Song.DoesNotExist):
            Song.objects.get(id=song.id)


class LyricViewTest(APITestCase):
    """
    Tests Lyric endpoints
    """

    def setUp(self):
        """
        Sets up Faker instance to be used on dummy word generation
        """

        Faker.seed()
        self.fake = Faker()
        super().setUp()

    def test_01_create_lyrics(self):
        """
        Tests lyric creation
        """

        # Lyric and song creation on-the-go
        artist = ArtistFactory()
        album = AlbumFactory(artist=artist)
        lyric_text = self.fake.paragraph(nb_sentences=3)
        song_name = self.fake.sentence(nb_words=6)
        lyric_dict = dict(text=lyric_text, song=dict(name=song_name, album=album.id))
        url = reverse("api_index")
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["text"], lyric_text)
        self.assertEqual(response.data["song"]["name"], song_name)
        self.assertEqual(response.data["album"]["id"], album.id)
        self.assertEqual(response.data["artist"]["id"], album.artist.id)

        # Lyric created with song id
        song = SongFactory()
        lyric_dict = dict(text=lyric_text, song=song.id)
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["text"], lyric_text)
        self.assertEqual(response.data["song"]["name"], song.name)
        self.assertEqual(response.data["album"]["id"], song.album.id)
        self.assertEqual(response.data["artist"]["id"], song.album.artist.id)

        # Lyric created with incomplete song information
        lyric_dict = dict(
            text=lyric_text,
            song=dict(
                name=song_name,
            ),
        )
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Lyric created with inexistant album in song information
        lyric_dict = dict(text=lyric_text, song=dict(name=song_name, album=99999))
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Lyric created with wrong album information in song information
        lyric_dict = dict(
            text=lyric_text, song=dict(name=song_name, album=dict(name="New album"))
        )
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Lyric created with wrong song structure
        lyric_dict = dict(text=lyric_text, song=dict(album=album.id))
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Lyric created with no song id
        lyric_dict = dict(text=lyric_text, song="Some name song")
        response = self.client.post(url, data=lyric_dict, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_02_upvote_downvote_lyrics(self):
        """
        Tests lyric upvote and downvote endpoints
        """

        # Upvote
        lyric = LyricFactory()
        response = self.client.get(reverse("upvote_lyric", kwargs=dict(pk=lyric.id)))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["id"], lyric.id)
        self.assertEqual(response.data["votes"], lyric.votes + 1)
        self.assertEqual(response.data["upvotes"], lyric.upvotes + 1)

        # Downvote
        response = self.client.get(reverse("downvote_lyric", kwargs=dict(pk=lyric.id)))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["id"], lyric.id)
        self.assertEqual(response.data["votes"], lyric.votes + 2)
        self.assertEqual(response.data["downvotes"], lyric.upvotes + 1)

    def test_03_random_lyrics(self):
        """
        Tests random lyric retrieval
        """

        # Basic random lyrics
        response = self.client.get(reverse("random_lyric"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        lyric_id = response.data["id"]
        self.assertEqual(response.data["text"], Lyric.objects.get(id=lyric_id).text)
        lyric = LyricFactory(song=Lyric.objects.first().song)

        # Random lyrics with artist id
        response = self.client.get(
            reverse("random_lyric") + f"?artist_id={lyric.song.album.artist.id}"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["artist"]["id"], lyric.song.album.artist.id)
        self.assertEqual(response.data["artist"]["name"], lyric.song.album.artist.name)

        # Random lyrics with artist name
        response = self.client.get(
            reverse("random_lyric") + f"?artist={lyric.song.album.artist.name}"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["artist"]["id"], lyric.song.album.artist.id)
        self.assertEqual(response.data["artist"]["name"], lyric.song.album.artist.name)

        # Random lyrics with nonexistant artist
        response = self.client.get(
            reverse("random_lyric") + f"?artist=someinventedartist"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, dict())

    def test_04_retrieve_all_lyrics(self):
        """
        Tests lyric retrieval of all lyrics
        """

        response = self.client.get(reverse("api_index") + f"?size=1000")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Lyric.objects.count())

    def test_05_retrieve_lyric(self):
        """
        Tests lyric retrieval of an specific lyric
        """

        lyric = LyricFactory()
        response = self.client.get(reverse("api_detail", kwargs=dict(pk=lyric.id)))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["id"], lyric.id)
        self.assertEqual(response.data["text"], lyric.text)
        self.assertEqual(response.data["song"]["id"], lyric.song.id)
        self.assertEqual(response.data["album"]["id"], lyric.song.album.id)
        self.assertEqual(response.data["artist"]["id"], lyric.song.album.artist.id)

    def test_03_delete_lyric(self):
        """
        Tests lyric retrieval
        """

        lyric = LyricFactory()
        response = self.client.delete(reverse("api_detail", kwargs=dict(pk=lyric.id)))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(Lyric.DoesNotExist):
            Lyric.objects.get(id=lyric.id)
