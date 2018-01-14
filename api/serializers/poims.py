from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from api.models import POIM, POIMImage

from .change_requests import ChangeRequestSerializer
from .comments import CommentSerializer
from .ratings import MyRatingSerializer
from .tags import TagsField
from .users import BasicUserSerializer


class POIMImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = POIMImage
        fields = ('photo',)


class POIMSerializer(serializers.HyperlinkedModelSerializer):
    owner = BasicUserSerializer(read_only=True)
    tags = TagsField()
    photos = POIMImageSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    change_requests = ChangeRequestSerializer(many=True, read_only=True)
    positive_ratings_count = serializers.IntegerField(read_only=True)
    negative_ratings_count = serializers.IntegerField(read_only=True)
    is_visited = serializers.BooleanField(read_only=True)
    my_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = POIM
        fields = ('id', 'name', 'owner', 'description', 'location', 'status', 'severity',
                  'created_date', 'updated_date', 'url', 'is_visited', 'my_rating',
                  'tags', 'photos', 'comments', 'change_requests',
                  'positive_ratings_count', 'negative_ratings_count')
        read_only_fields = ('status',)

    def get_my_rating(self, obj):
        try:
            my_rating = obj.ratings.get(owner_id=self.context['request'].user.id or 0)
            return MyRatingSerializer(my_rating).data
        except ObjectDoesNotExist:
            return None


class POIMListSerializer(serializers.HyperlinkedModelSerializer):
    is_visited = serializers.BooleanField(read_only=True)

    class Meta:
        model = POIM
        fields = ('id', 'name', 'location', 'status', 'severity', 'url', 'is_visited')
