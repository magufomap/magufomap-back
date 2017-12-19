from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from api.models import POI, POIImage, Rating, Comment
from mapwidgets.widgets import GooglePointFieldWidget


class ImageInline(admin.TabularInline):
    model = POIImage

class RatingInline(admin.TabularInline):
    model = Rating

class CommentInline(admin.TabularInline):
    model = Comment

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    
class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    inlines = [
            ImageInline,
            RatingInline,
            CommentInline
    ]


admin.site.register(POI, POIAdmin)
admin.site.register(Comment, CommentAdmin)
