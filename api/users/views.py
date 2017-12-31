from rest_framework import mixins, viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
