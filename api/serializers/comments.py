from rest_framework import serializers

from api.models import Comment

from .users import BasicUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "poim", "owner", "comment", "created_date")
