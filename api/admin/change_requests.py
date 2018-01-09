from django.contrib import admin

from api.models import ChangeRequest


class ChangeRequestEditorInline(admin.TabularInline):
    model = ChangeRequest
    readonly_fields = ["owner", "change"]
    extra = 0


class ChangeRequestInline(admin.TabularInline):
    model = ChangeRequest
    extra = 0


class ChangeRequestAdmin(admin.ModelAdmin):
    model = ChangeRequest

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # si no es superuser, solo puede ver los change request que ha hecho
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
        return ("poim", "owner", "change")
