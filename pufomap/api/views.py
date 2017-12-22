from django.contrib.auth.models import User
from django.db.models import Count, Case, Value, When, Exists, OuterRef, Subquery
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter
from api.filters import POIFilter
from api.models import POI, Comment, Rating, Visited, ChangeRequest
from api.serializers import UserSerializer, POIDetailSerializer, POIListSerializer, TagSerializer, ListCommentSerializer, RetrieveCommentSerializer, RatingSerializer, CreateCommentSerializer, RetrieveVisitedSerializer, RetrieveChangeRequestSerializer, ListChangeRequestSerializer, CreateChangeRequestSerializer, POIChangeRequestsListSerializer
from taggit.models import Tag


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, *args, **kwargs):
        user = User.objects.create_user(username=self.request.data['username'],
                                 email=self.request.data['email'],
                                 password=self.request.data['password'],
                                 is_staff=True)
        serializer = self.serializer_class(user, context={'request': self.request})
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the current user to see useful info
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self, request):
        user = get_object_or_404(self.queryset, id=self.request.user.id)
        serializer = self.serializer_class(user, context={'request': self.request})
        return Response(serializer.data)


class POIsWithChangeRequestsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the current user to see her POIs with change requests
    """
    queryset = POI.objects.all()
    serializer_class = POIChangeRequestsListSerializer
    def list(self, request):
        pois = self.queryset.filter(author_id=self.request.user.id).exclude(changerequests=None)
        serializer = self.serializer_class(pois, many=True, context={'request': self.request})
        return Response(serializer.data)


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
        self.request.data["user"] = self.request.user.id
        return viewsets.ModelViewSet.create(self, *args, **kwargs)


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.order_by('-created_date')

    def list(self, *args, **kwargs):
        self.serializer_class = ListChangeRequestSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = RetrieveChangeRequestSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)

    def create(self, *args, **kwargs):
        self.serializer_class = CreateChangeRequestSerializer
        self.request.data["user"] = self.request.user.id
        return viewsets.ModelViewSet.create(self, *args, **kwargs)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, *args, **kwargs):
        self.request.data["user"] = self.request.user.id
        return viewsets.ModelViewSet.create(self, *args, **kwargs)


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
            visited = Visited.objects.filter(
                    poi=OuterRef('pk'),
                    visited=True,
                    user_id=0
            )
            voted = Rating.objects.filter(
                    poi=OuterRef('pk'),
                    user_id=0
            ).values('vote')
            return self.queryset.filter(status='PUB')\
                    .annotate(visit=Exists(visited))\
                    .annotate(voted=Subquery(voted))\
                    .order_by('-updated_date')


        visited = Visited.objects.filter(
                poi=OuterRef('pk'),
                visited=True,
                user_id=self.request.user.id
        )
        voted = Rating.objects.filter(
                poi=OuterRef('pk'),
                user_id=self.request.user.id
        ).values('vote')
        return self.queryset\
                .annotate(visit=Exists(visited))\
                .annotate(voted=Subquery(voted))\
                .order_by('-updated_date')

    def list(self, *args, **kwargs):
        self.serializer_class = POIListSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = POIDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)
