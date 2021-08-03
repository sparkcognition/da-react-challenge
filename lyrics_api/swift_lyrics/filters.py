from django_filters import rest_framework as filters, NumberFilter, CharFilter

from swift_lyrics.models import Artist, Lyric


class ArtistFilter(filters.FilterSet):
	"""
	This class registers a new filter for Artist view
	"""

	class Meta:
		model = Artist
		fields = {
			'first_year_active': ['lt', 'gt'],
			'name': ['exact', 'contains'],
		}


class RandomLyricFilter(filters.FilterSet):
	"""
	This class adds support for Artist filtering
	"""

	artist_id = NumberFilter(
		field_name='song', lookup_expr='album__artist__id')
	artist = CharFilter(
		field_name='song', lookup_expr='album__artist__name__icontains')

	class Meta:
		model = Lyric
		fields = []
