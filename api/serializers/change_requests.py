from rest_framework import serializers

from api.models import ChangeRequest

from .users import BasicUserSerializer


class ChangeRequestSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = ChangeRequest
        fields = ("id", "poim", "owner", "change", "status", "created_date")
