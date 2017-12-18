from django.contrib import admin
from api.models import POI


class POIAdmin(admin.ModelAdmin):
    pass

admin.site.register(POI, POIAdmin)

