from rest_framework import serializers

from api.users.serializers import BasicUserSerializer

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "poim", "owner", "comment", "created_date")
