from django.apps import apps
from django.db import models
from django.contrib.gis.db import models as geomodels

from taggit.managers import TaggableManager
from slugify import UniqueSlugify

from api.choices import poims as choices


def unique_slug_checker(model_name):
    def func(text, uids):
        if text in uids:
            return False
        return not apps.get_model(model_name).objects.filter(slug=text).exists()
    return func


class POIM(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=False, blank=False, unique=True, db_index=True)
    location = geomodels.PointField(blank=False, null=False)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=choices.STATUSES, default=choices.PENDING)
    severity = models.IntegerField(choices=choices.SEVERITIES, default=1)
    tags = TaggableManager()
    owner = models.ForeignKey("api.User", on_delete=models.SET_NULL, null=True, related_name='poims')
    created_date = models.DateTimeField(blank=True, null=False, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    _slug_generator = UniqueSlugify(max_length=250, to_lower=True,
                                    unique_check=unique_slug_checker('api.POIM'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self._slug_generator(self.name)

        return super().save(*args, **kwargs)


class POIMImage(models.Model):
    poim = models.ForeignKey('POIM', related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(blank=False, null=False, upload_to='uploads')
