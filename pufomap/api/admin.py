from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from api.models import POI
from mapwidgets.widgets import GooglePointFieldWidget


class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(POI, POIAdmin)
