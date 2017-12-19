from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from api.models import POI, POIImage, Comment
from taggit.models import Tag
from rest_framework import serializers
from rest_framework.exceptions import ParseError

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug","name")

class TagSerializerField(serializers.ListField):

    ## Requires support for DRF browseable interface
    def to_internal_value(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_representation(self, obj):
       if type(obj) is not list:
            return [tag.name for tag in obj.all()]
       return obj


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class POIImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = POIImage
        fields = ('id', 'photo')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'created_date')
        
class POIDetailSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializerField()
    photos = POIImageSerializer(many=True)
#    poi_comments = serializers.StringRelatedField(many=True)
#    poi_comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    poi_comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = POI
        fields = ('name', 'description', 'status', 'severity', 'tags', 'positive_ratings_count', 'negative_ratings_count', 'created_date', 'updated_date', 'photos', 'url', 'location', 'poi_comments')


class POIListSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializerField()

    class Meta:
        model = POI
        fields = ('name', 'status', 'severity', 'tags', 'url', 'location')
