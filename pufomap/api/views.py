from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import UserSerializer
from api.models import POI
from api.serializers import POISerializer

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
    queryset = POI.objects.all()
    serializer_class = POISerializer
