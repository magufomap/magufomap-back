from rest_framework import viewsets

from api.utils.permissions import IsOwnerOrReadOnly

from api.models import ChangeRequest
from api.serializers import ChangeRequestSerializer


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.all().order_by('-created_date', 'id')
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
