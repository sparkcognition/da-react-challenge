from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase, APIClient

from faker import Faker 

from swift_lyrics.models import Album, Artist, Lyric, Song
from swift_lyrics.factories import (
	AlbumFactory,
	ArtistFactory,
	LyricFactory,
	SongFactory,
)
from swift_lyrics.views import (
	AlbumIndex,
)


class HealthCheckTest(APITestCase):

	def test_01_healthcheck(self):
		response = self.client.get(reverse('health'))
		self.assertEqual(response.status_code, HTTP_200_OK)


class AlbumViewTest(APITestCase):

	def setUp(self):
		super().setUp()

	def album_index(self):
		return reverse('album_index')

	def album_detail(self, pk):
		return reverse('album_detail', kwargs={"pk": pk})

	def test_01_retrieve_all_albums(self):
		response = self.client.get(self.album_index() + f'?size=100')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(len(response.data['results']), Album.objects.count())

	def test_02_retrieve_album(self):
		album = AlbumFactory()
		response = self.client.get(self.album_detail(album.id))
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['id'], album.id)
		self.assertEqual(response.data['year'], album.year)
		self.assertEqual(response.data['name'], album.name)

	def test_03_create_album(self):
		first_album_name = "The awesome album"
		first_album_year = 2011
		album_artist = "Mouse Rat"
		body = dict(
			name=first_album_name,
			year=first_album_year,
			artist=dict(
				name=album_artist,
				first_year_active=2008,
			)	
		)
		response = self.client.post(self.album_index(), data=body, format='json')
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		self.assertEqual(response.data['name'], first_album_name)
		self.assertEqual(response.data['year'], first_album_year)
		self.assertEqual(response.data['artist']['name'], album_artist)
		album_artist_id = response.data['artist']['id']
		second_album_name = "The awesome follow-up album"
		second_album_year = 2013
		body = dict(
			name=second_album_name,
			year=second_album_year,
			artist=dict(
				name=album_artist,
			)	
		)
		response = self.client.post(self.album_index(), data=body, format='json')
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		self.assertEqual(response.data['name'], second_album_name)
		self.assertEqual(response.data['year'], second_album_year)
		self.assertEqual(response.data['artist']['name'], album_artist)
		third_album_name = "The last album"
		third_album_year = 2015
		body = dict(
			name=third_album_name,
			year=third_album_year,
			artist=album_artist_id,
		)
		response = self.client.post(self.album_index(), data=body, format='json')
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		self.assertEqual(response.data['name'], third_album_name)
		self.assertEqual(response.data['year'], third_album_year)
		self.assertEqual(response.data['artist']['name'], album_artist)

	def test_04_create_album_error(self):
		response = self.client.post(self.album_index(), data=dict(), format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		no_artist_dict = dict(
			name="Some artist",
			year=2013,
			artist=dict()
		)
		response = self.client.post(self.album_index(), data=no_artist_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		no_year_in_artist_dict = dict(
			name="Some artist",
			year=2013,
			artist=dict(
				name="Unknown artist"
			)
		)
		response = self.client.post(self.album_index(), data=no_year_in_artist_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

	def test_05_delete_album(self):
		album = Album.objects.first()
		response = self.client.delete(self.album_detail(album.id))
		self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
		with self.assertRaises(Album.DoesNotExist):
			Album.objects.get(id=album.id)


class ArtistViewTest(APITestCase):

	def setUp(self):
		super().setUp()

	def test_01_retrieve_artists(self):
		url = reverse('artist-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(len(response.data['results']), Artist.objects.count())
		artist = Artist.objects.first()
		url = reverse('artist-list') + f'?first_year_active__lt={artist.first_year_active}'
		response = self.client.get(url)
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(
			len(response.data['results']),
			Artist.objects.filter(
				first_year_active__lt=artist.first_year_active).count())
		url = reverse('artist-list') + f'?first_year_active__gt={artist.first_year_active}'
		response = self.client.get(url)
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(
			len(response.data['results']),
			Artist.objects.filter(
				first_year_active__gt=artist.first_year_active).count())
		url = reverse('artist-list') + f'?name={artist.name}'
		response = self.client.get(url)
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(
			len(response.data['results']), 1)

	def test_02_retrieve_single_artist(self):
		artist = ArtistFactory()
		url = reverse('artist-detail', kwargs=dict(pk=artist.id))
		response = self.client.get(url)
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['id'], artist.id),
		self.assertEqual(response.data['name'], artist.name)
		self.assertEqual(response.data['first_year_active'], artist.first_year_active)

	def test_03_create_single_artist(self):
		artist_name = "The zombielites"
		artist_year = 2011
		artist_dict = dict(
			name=artist_name,
			first_year_active=artist_year,
		)
		url = reverse('artist-list')
		response = self.client.post(url, data=artist_dict, format='json')
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		self.assertEqual(response.data['name'], artist_name)
		self.assertEqual(response.data['first_year_active'], artist_year)

	def test_04_update_single_artist(self):
		artist = Artist.objects.first()
		artist_name = "New artist name"
		artist_dict = dict(name=artist_name)
		url = reverse('artist-detail', kwargs=dict(pk=artist.id))
		response = self.client.patch(url, data=artist_dict, format='json')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['name'], artist_name)

	def test_05_delete_artist(self):
		artist = Artist.objects.first()
		url = reverse('artist-detail', kwargs=dict(pk=artist.id))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
		with self.assertRaises(Artist.DoesNotExist):
			Artist.objects.get(id=artist.id)


class SongViewTest(APITestCase):

	def setUp(self):
		super().setUp()

	def test_01_retrieve_all_songs(self):
		response = self.client.get(reverse('song_index') + f'?size=100')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(len(response.data['results']), Song.objects.count())

	def test_02_retrieve_song(self):
		song = SongFactory()
		response = self.client.get(reverse('song_detail', kwargs=dict(pk=song.id)))
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['id'], song.id)
		self.assertEqual(response.data['name'], song.name)
		self.assertEqual(response.data['album']['id'], song.album.id)
		self.assertEqual(response.data['album']['artist']['id'], song.album.artist.id)

	def test_03_delete_song(self):
		song = SongFactory()
		response = self.client.delete(reverse('song_detail', kwargs=dict(pk=song.id)))
		self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
		with self.assertRaises(Song.DoesNotExist):
			Song.objects.get(id=song.id)


class LyricsViewTest(APITestCase):

	def setUp(self):
		Faker.seed()
		self.fake = Faker()
		super().setUp()

	def test_01_create_lyrics(self):
		artist = ArtistFactory()
		album = AlbumFactory(artist=artist)
		lyric_text = self.fake.paragraph(nb_sentences=3)
		song_name = self.fake.sentence(nb_words=6)
		lyric_dict = dict(
			text=lyric_text,
			song=dict(
				name=song_name,
				album=album.id
			)
		)
		url = reverse('api_index')
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		self.assertEqual(response.data['text'], lyric_text)
		self.assertEqual(response.data['song']['name'], song_name)
		self.assertEqual(response.data['album']['id'], album.id)
		self.assertEqual(response.data['artist']['id'], album.artist.id)
		song = SongFactory()
		lyric_dict = dict(
			text=lyric_text,
			song=song.id
		)
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		self.assertEqual(response.data['text'], lyric_text)
		self.assertEqual(response.data['song']['name'], song.name)
		self.assertEqual(response.data['album']['id'], song.album.id)
		self.assertEqual(response.data['artist']['id'], song.album.artist.id)
		lyric_dict = dict(
			text=lyric_text,
			song=dict(
				name=song_name,
			)
		)
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		lyric_dict = dict(
			text=lyric_text,
			song=dict(
				name=song_name,
				album=99999
			)
		)
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		lyric_dict = dict(
			text=lyric_text,
			song=dict(
				name=song_name,
				album=dict(name="New album")
			)
		)
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		lyric_dict = dict(
			text=lyric_text,
			song=dict(
				album=album.id
			)
		)
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		lyric_dict = dict(
			text=lyric_text,
			song="Some name song"
		)
		response = self.client.post(url, data=lyric_dict, format='json')
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

	def test_02_upvote_downvote_lyrics(self):
		lyric = LyricFactory()
		response = self.client.get(reverse('upvote_lyric', kwargs=dict(pk=lyric.id)))
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['id'], lyric.id)
		self.assertEqual(response.data['votes'], lyric.votes+1)
		self.assertEqual(response.data['upvotes'], lyric.upvotes+1)
		response = self.client.get(reverse('downvote_lyric', kwargs=dict(pk=lyric.id)))
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['id'], lyric.id)
		self.assertEqual(response.data['votes'], lyric.votes+2)
		self.assertEqual(response.data['downvotes'], lyric.upvotes+1)

	def test_03_random_lyrics(self):
		response = self.client.get(reverse('random_lyric'))
		self.assertEqual(response.status_code, HTTP_200_OK)
		lyric_id = response.data['id']
		self.assertEqual(response.data['text'], Lyric.objects.get(id=lyric_id).text)
		lyric = LyricFactory(song=Lyric.objects.first().song)
		response = self.client.get(reverse('random_lyric') + f'?artist_id={lyric.song.album.artist.id}')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['artist']['id'], lyric.song.album.artist.id)
		self.assertEqual(response.data['artist']['name'], lyric.song.album.artist.name)
		response = self.client.get(reverse('random_lyric') + f'?artist={lyric.song.album.artist.name}')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['artist']['id'], lyric.song.album.artist.id)
		self.assertEqual(response.data['artist']['name'], lyric.song.album.artist.name)
		response = self.client.get(reverse('random_lyric') + f'?artist=someinventedartist')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data, dict())

	def test_04_retrieve_all_lyrics(self):
		response = self.client.get(reverse('api_index') + f'?size=1000')
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(len(response.data['results']), Lyric.objects.count())

	def test_05_retrieve_lyric(self):
		lyric = LyricFactory()
		response = self.client.get(reverse('api_detail', kwargs=dict(pk=lyric.id)))
		self.assertEqual(response.status_code, HTTP_200_OK)
		self.assertEqual(response.data['id'], lyric.id)
		self.assertEqual(response.data['text'], lyric.text)
		self.assertEqual(response.data['song']['id'], lyric.song.id)
		self.assertEqual(response.data['album']['id'], lyric.song.album.id)
		self.assertEqual(response.data['artist']['id'], lyric.song.album.artist.id)

	def test_03_delete_lyric(self):
		lyric = LyricFactory()
		response = self.client.delete(reverse('api_detail', kwargs=dict(pk=lyric.id)))
		self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
		with self.assertRaises(Lyric.DoesNotExist):
			Lyric.objects.get(id=lyric.id)
