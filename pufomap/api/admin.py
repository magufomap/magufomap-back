from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from api.models import POI, POIImage, Rating, Comment, Visited
from mapwidgets.widgets import GooglePointFieldWidget


class ImageInline(admin.TabularInline):
    model = POIImage

class RatingInline(admin.TabularInline):
    model = Rating

class CommentInline(admin.TabularInline):
    model = Comment
    
class CommentAdmin(admin.ModelAdmin):
    model = Comment

class RatingInline(admin.TabularInline):
    model = Rating
    
class RatingAdmin(admin.ModelAdmin):
    model = Rating

class VisitedInline(admin.TabularInline):
    model = Visited
    
class VisitedAdmin(admin.ModelAdmin):
    model = Visited

    
class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    inlines = [
            ImageInline,
            RatingInline,
            CommentInline,
            RatingInline,
            VisitedInline
    ]


admin.site.register(POI, POIAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Visited, VisitedAdmin)
