from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from api.models import POI, POIImage, Rating
from mapwidgets.widgets import GooglePointFieldWidget


class ImageInline(admin.TabularInline):
    model = POIImage

class RatingInline(admin.TabularInline):
    model = Rating

class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    inlines = [
            ImageInline,
            RatingInline
    ]


admin.site.register(POI, POIAdmin)
