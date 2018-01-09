from rest_framework import serializers
from rest_framework.exceptions import ParseError
from taggit.models import Tag


class TagsField(serializers.ListField):
    def to_internal_value(self, data):
        # Requires support for DRF browseable interface
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")
