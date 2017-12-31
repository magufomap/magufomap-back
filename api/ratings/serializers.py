from rest_framework import serializers

from api.users.serializers import BasicUserSerializer

from .models import Rating


class MyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "poim", "vote")


class RatingSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ("id", "owner", "poim", "vote")
