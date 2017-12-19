from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels

from taggit.managers import TaggableManager


STATUS = (
    ("PUB","Publicada"),
    ("PEN","Pendiente"),
    ("INV","No válida"),
    )


class POI(models.Model):
    #author = models.ForeignKey('User', on_delete=models.SET(get_admin_user))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    location = geomodels.PointField(blank=False, null=True)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default="PEN")
    severity = models.IntegerField()
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


class POIImage(models.Model):
    poi = models.ForeignKey('POI', related_name='photos',
            on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads',
            blank=False, null=False)
