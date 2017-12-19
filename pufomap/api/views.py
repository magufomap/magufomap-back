from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework_gis.filters import InBBoxFilter
from api.serializers import UserSerializer
from api.models import POI
from api.serializers import POISerializer
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class POIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows POIs to be viewed or edited.
    """
    queryset = POI.objects.order_by('-updated_date')
    serializer_class = POISerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, DjangoFilterBackend)
    bbox_filter_include_overlapping = True
    filter_fields = ('severity',)
