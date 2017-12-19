from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework_gis.filters import InBBoxFilter
from api.serializers import UserSerializer
from api.models import POI
from api.serializers import POIDetailSerializer, POIListSerializer
from django_filters import rest_framework as filters

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class POIFilter(filters.FilterSet):
    class Meta:
        model = POI
        fields = {
            'severity': ['exact', 'in', ]
        }


class POIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows POIs to be viewed or edited.
    """
    queryset = POI.objects.order_by('-updated_date')
    #serializer_class = POISerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend)
    bbox_filter_include_overlapping = True
    filter_class = POIFilter
    filter_fields = ('severity',)

    def list(self, *args, **kwargs):
        self.serializer_class = POIListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = POIDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)
