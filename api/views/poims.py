from django.db.models import Case, Count, IntegerField, Q, Sum, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_gis.filters import InBBoxFilter

from api.choices import poims as choices
from api.filters.poims import POIMFilter
from api.models import POIM
from api.serializers import POIMSerializer, POIMListSerializer

from api.utils.permissions import IsOwnerOrReadOnly
from api.utils.viewsets import MultiSerializerViewSetMixin


class POIMViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = POIM.objects.all().order_by('-updated_date', 'id')
    serializer_class = POIMSerializer
    serializer_action_classes = {
        'list': POIMListSerializer
    }
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (InBBoxFilter, DjangoFilterBackend)
    filter_class = POIMFilter
    bbox_filter_field = 'location'
    bbox_filter_include_overlapping = True

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        # Filter no published POIMS (for anonymous users)
        if self.request.user.is_anonymous:
            queryset = queryset.filter(status=choices.PUBLISHED)

        # Count rattings (for detail view)
        if (self.action == 'retrieve'):
            queryset = queryset.annotate(
                positive_ratings_count=Count('ratings', filter=Q(ratings__vote=1), distinct=True),
                negative_ratings_count=Count('ratings', filter=Q(ratings__vote=-1), distinct=True)
            )

        # is visited by me?
        queryset = queryset.annotate(is_visited=Sum(Case(
            When(ratings__owner_id=(self.request.user.id or 0), then=1),
            When(comments__owner_id=(self.request.user.id or 0), then=1),
            When(change_requests__owner_id=(self.request.user.id or 0), then=1),
            When(owner_id=(self.request.user.id or 0), then=1),
            default=0,
            output_field=IntegerField()
        )))

        return queryset
