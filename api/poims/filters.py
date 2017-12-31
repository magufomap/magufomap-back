from django_filters import rest_framework as filters

from .models import POIM


class POIMFilter(filters.FilterSet):
    class Meta:
        model = POIM
        fields = {
            'severity': ['exact', 'in'],
            'tags__name': ['exact', 'in'],
            'status': ['exact', 'in']
        }
