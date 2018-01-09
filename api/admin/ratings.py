from django.contrib import admin

from api.models import Rating


class RatingEditorInline(admin.TabularInline):
    model = Rating
    readonly_fields = ["owner", "poim", "vote"]
    extra = 0


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    model = Rating

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # just show their ratings
        return super().get_queryset(request).filter(owner=request.user)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser and "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # only superusers can edit comments
        return ("poim", "owner", "vote")
