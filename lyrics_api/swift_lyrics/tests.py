from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from swift_lyrics.models import Lyric

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

    def test_vote_up_unauthenticated(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        response = self.client.post(reverse('lyric-vote-up', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # reload lyric from DB
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(count_votes_before, lyric.votes)

    def test_vote_down_unauthenticated(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        response = self.client.post(reverse('lyric-vote-down', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # reload lyric from DB
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(count_votes_before, lyric.votes)

    def test_vote_up_authenticated(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        self.client.login(username=TEST_ACCOUNT_USERNAME, password=TEST_ACCOUNT_PASSWORD)
        response = self.client.post(reverse('lyric-vote-up', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(lyric.votes, count_votes_before + 1)

    def test_vote_down_authenticated(self):
        lyric = Lyric.objects.first()
        count_votes_before = lyric.votes
        self.client.login(username=TEST_ACCOUNT_USERNAME, password=TEST_ACCOUNT_PASSWORD)
        response = self.client.post(reverse('lyric-vote-down', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(lyric.votes, count_votes_before - 1)

    def test_create_without_album_id(self):
        data = {
            'text': 'la la la, lo lo lo',
            'album': {
                'name': 'Album 1'
            }
        }
        response = self.client.post(reverse('lyric-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)