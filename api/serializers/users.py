from rest_framework import serializers
from django_gravatar.helpers import get_gravatar_url

from api.models import User


class BasicUserSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "full_name", "url", "photo")

    def get_photo(self, obj):
        return get_gravatar_url(obj.email)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "url")
