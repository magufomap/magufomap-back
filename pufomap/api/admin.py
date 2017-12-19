from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from api.models import POI, POIImage
from mapwidgets.widgets import GooglePointFieldWidget


class ImageInline(admin.TabularInline):
    model = POIImage


class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    inlines = [
            ImageInline
    ]


admin.site.register(POI, POIAdmin)
