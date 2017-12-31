from rest_framework import serializers

from api.users.serializers import BasicUserSerializer

from .models import ChangeRequest


class ChangeRequestSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = ChangeRequest
        fields = ("id", "poim", "owner", "change", "status", "created_date")
