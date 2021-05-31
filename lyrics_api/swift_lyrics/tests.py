from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from swift_lyrics.models import Artist, Lyric

TEST_ACCOUNT_PASSWORD = '123'
TEST_ACCOUNT_USERNAME = 'test'
TEST_ACCOUNT_EMAIL = 'test@local'


class LyricTests(APITestCase):

    def setUp(self):
        user = User(username=TEST_ACCOUNT_USERNAME, email=TEST_ACCOUNT_EMAIL)
        user.set_password(TEST_ACCOUNT_PASSWORD)
        user.save()

    def test_list(self):
        count_before = Lyric.objects.count()
        response = self.client.get(reverse('lyric-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count_before)

    def test_vote_up_unauthenticated_fails(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        response = self.client.post(reverse('lyric-vote-up', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # reload lyric from DB
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(count_votes_before, lyric.votes)

    def test_vote_down_unauthenticated_fails(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        response = self.client.post(reverse('lyric-vote-down', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # reload lyric from DB
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(count_votes_before, lyric.votes)

    def test_vote_up_authenticated_succeed(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        self.client.login(username=TEST_ACCOUNT_USERNAME, password=TEST_ACCOUNT_PASSWORD)
        response = self.client.post(reverse('lyric-vote-up', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(lyric.votes, count_votes_before + 1)

    def test_vote_down_authenticated_succeed(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        self.client.login(username=TEST_ACCOUNT_USERNAME, password=TEST_ACCOUNT_PASSWORD)
        response = self.client.post(reverse('lyric-vote-down', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(lyric.votes, count_votes_before - 1)

    def test_create_without_album_id_fails(self):
        data = {
            'text': 'la la la, lo lo lo',
            'album': {
                'name': 'Album 1'
            }
        }
        response = self.client.post(reverse('lyric-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shuffle_with_non_existent_artist_fails(self):
        non_existent_artist_name = 'foobar'
        # make sure that artist doesn't exist
        self.assertEqual(Artist.objects.filter(name=non_existent_artist_name).count(), 0)
        response = self.client.get(f"{reverse('lyric-shuffle')}?artist={non_existent_artist_name}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AlbumTests(APITestCase):

    def test_create_without_year_fails(self):
        data = {
            'name': 'Thriller',
            'artist_name': 'Michael Jackson'
        }
        response = self.client.post(reverse('album-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArtistTest(APITestCase):

    def test_list(self):
        response = self.client.get(reverse('artist-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # make sure that each artist includes id, name and first_year_active
        # in response but not albums
        for result in response.data['results']:
            self.assertIn('id', result)
            self.assertIn('name', result)
            self.assertIn('first_year_active', result)
            self.assertNotIn('albums', result)

    def test_detail(self):
        artist = Artist.objects.first()
        response = self.client.get(reverse('artist-detail', args=[artist.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = response.data
        self.assertIn('id', item)
        self.assertIn('name', item)
        self.assertIn('first_year_active', item)
        self.assertIn('albums', item)
