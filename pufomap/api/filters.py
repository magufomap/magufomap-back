from api.models import POI
from django_filters import rest_framework as filters


class POIFilter(filters.FilterSet):

    class Meta:
        model = POI
        fields = {
            'severity': ['exact', 'in'],
            'tags__name': ['exact', 'in'],
            'status': ['exact', 'in']
        }
