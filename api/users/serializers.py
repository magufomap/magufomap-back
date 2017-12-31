from rest_framework import serializers

from .models import User


class BasicUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "url")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("username", "full_name", "url")
