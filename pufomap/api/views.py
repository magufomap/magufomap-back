from django.contrib.auth.models import User
from django.db.models import Count, Case, Value, When
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework_gis.filters import InBBoxFilter
from api.filters import POIFilter
from api.models import POI, Comment, Rating, Visited
from api.serializers import UserSerializer, POIDetailSerializer, POIListSerializer, TagSerializer, ListCommentSerializer, RetrieveCommentSerializer, RatingSerializer, CreateCommentSerializer, RetrieveVisitedSerializer
from taggit.models import Tag

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class VisitedViewSet(viewsets.ModelViewSet):
    queryset = Visited.objects.all()
    serializer_class = RetrieveVisitedSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-created_date')

    def list(self, *args, **kwargs):
        self.serializer_class = ListCommentSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = RetrieveCommentSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)

    def create(self, *args, **kwargs):
        self.serializer_class = CreateCommentSerializer
        return viewsets.ModelViewSet.create(self, *args, **kwargs)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class POIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows POIs to be viewed or edited.
    """
    queryset = POI.objects.order_by('-updated_date')
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend)
    bbox_filter_include_overlapping = True
    filter_class = POIFilter
    filter_fields = ('severity',)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_anonymous:
                #.annotate(visit=Count('poi_visits__user'))
            return POI.objects.filter(status='PUB').order_by('-updated_date') \
                .annotate(visit=Count('poi_visits__user'))
                #.annotate(visit=Case(
                #    #When(self.request.user.pk in [uv['user_visits'] for uv in poi for poi.visited.all().values('user_visits') in self.queryset],
                #    When(self.request.user.pk in [poi.visited.all().values('user_visits') for poi in self.queryset],
                #         then=Value(1)),
                #    default=Value(0),
                #    output_field=BooleanField()))

        return self.queryset.annotate(visit=Count('visited'))

    def list(self, *args, **kwargs):
        self.serializer_class = POIListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = POIDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)
