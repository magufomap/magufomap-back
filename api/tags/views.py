from rest_framework import mixins, viewsets
from taggit.models import Tag

from .serializers import TagSerializer


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
