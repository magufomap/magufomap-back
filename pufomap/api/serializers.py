from django.contrib.auth.models import User
from api.models import POI
from rest_framework import serializers
from rest_framework.exceptions import ParseError

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

class POISerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializerField()    
    class Meta:

        model = POI
        fields = ('name','description','status','severity','tags','created_date','updated_date')
        
