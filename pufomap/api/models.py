from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels

from photologue.models import Gallery
from taggit.managers import TaggableManager

# Create your models here.

STATUS = (
    ("PUB","Publicada"),
    ("PEN","Pendiente"),
    ("INV","No válida"),
    )


#def get_admin_user():
#    return User.objects.get(username='yami')

class POI(models.Model):
    #author = models.ForeignKey('User', on_delete=models.SET(get_admin_user))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    location = geomodels.PointField(blank=False, null=True)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default="PEN")
    severity = models.IntegerField()
    photos = models.OneToOneField(Gallery,
            related_name='poi',
            on_delete=models.DO_NOTHING,
            null=True, blank=True)
    tags = TaggableManager()
    created_date = models.DateTimeField(
            blank=True, null=False,
            auto_now_add=True
    )
    updated_date = models.DateTimeField(
            blank=True, null=True,
            auto_now=True,
    )

    def __str__(self):
        return self.name
