from django.db import models
from django.contrib.gis.db import models as geomodels

from taggit.managers import TaggableManager

from api.choices import poims as choices


class POIM(models.Model):
    name = models.CharField(max_length=200)
    location = geomodels.PointField(blank=False, null=True)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=choices.STATUSES, default=choices.PENDING)
    severity = models.IntegerField(choices=choices.SEVERITIES, default=1)
    tags = TaggableManager()
    owner = models.ForeignKey("api.User", on_delete=models.SET_NULL, null=True, related_name='poims')
    created_date = models.DateTimeField(blank=True, null=False, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name


class POIMImage(models.Model):
    poim = models.ForeignKey('POIM', related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(blank=False, null=False, upload_to='uploads')
