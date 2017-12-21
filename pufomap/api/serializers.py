from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from api.models import POI, POIImage, Comment, Rating, Visited, ChangeRequest
from taggit.models import Tag
from rest_framework import serializers
from rest_framework.exceptions import ParseError
import random

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

class BasicUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'id')


class RetrieveVisitedSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    class Meta:
        model = Visited
        fields = ('user', 'poi', 'visited')

class RetrieveBasicVisitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visited
        fields = ('poi', 'visited')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_visits = RetrieveBasicVisitedSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'user_visits')


class POIImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = POIImage
        fields = ('id', 'photo')


class RetrieveCommentSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'poi', 'comment', 'created_date')


class ListCommentSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'poi', 'comment', 'created_date')


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'poi', 'comment', 'created_date')


class ListChangeRequestSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    class Meta:
        model = ChangeRequest
        fields = ('user', 'poi', 'change', 'created_date')

class RetrieveChangeRequestSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    class Meta:
        model = ChangeRequest
        fields = ('user', 'poi', 'change', 'created_date')

class CreateChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = ('user', 'poi', 'change', 'created_date')

        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'poi', 'vote')

class POIDetailSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializerField()
    photos = POIImageSerializer(many=True)
    poi_comments = RetrieveCommentSerializer(many=True, read_only=True)
    visit = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()
    author = BasicUserSerializer()

    def get_voted(self, obj):
        return obj.voted

    def get_visit(self, obj):
        return obj.visit

    class Meta:
        model = POI
        fields = ('id', 'author', 'visit', 'name', 'description',
                  'status', 'severity', 'tags',
                  'positive_ratings_count', 'negative_ratings_count',
                  'created_date', 'updated_date', 'photos', 'url',
                  'location', 'poi_comments', 'voted')


class POIListSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializerField()
    visit = serializers.SerializerMethodField()
    author = BasicUserSerializer()
    voted = serializers.SerializerMethodField()

    def get_voted(self, obj):
        return obj.voted

    def get_visit(self, obj):
        return obj.visit


    class Meta:
        model = POI
        fields = ('id', 'visit', 'author', 'name',
                  'status', 'severity', 'tags', 'url', 'location',
                  'voted')
