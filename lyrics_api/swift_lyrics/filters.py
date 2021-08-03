from django_filters import rest_framework as filters, NumberFilter

from swift_lyrics.models import Artist


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
