from django.contrib import admin
from django.contrib.gis.db import models as geomodels

from mapwidgets.widgets import GooglePointFieldWidget

from api.comments.admin import CommentEditorInline, CommentInline
from api.change_requests.admin import ChangeRequestEditorInline, ChangeRequestInline
from api.ratings.admin import RatingEditorInline, RatingInline


from . import models


class POIMImageInline(admin.TabularInline):
    model = models.POIMImage
    extra = 0


@admin.register(models.POIM)
class POIMAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    inlines = [
        POIMImageInline,
    ]
    admin_inlines = [
        ChangeRequestInline,
        RatingInline,
        CommentInline
    ]
    editor_inlines = [
        ChangeRequestEditorInline,
        RatingEditorInline,
        CommentEditorInline
    ]
    exclude = ['owner']

    def get_inline_instances(self, request, obj):
        if request.user.is_superuser:
            inlines = self.inlines + self.admin_inlines
            return [inline(self.model, self.admin_site) for inline in inlines]

        # only show inlines for editors
        inlines = self.inlines + self.editor_inlines
        return [inline(self.model, self.admin_site) for inline in inlines]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # only show their own POIMs
        return super().get_queryset(request).filter(owner=request.user)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # only superusers can edit the status
        return ('status',)
