from django.contrib import admin

from api.models import Comment


class CommentEditorInline(admin.TabularInline):
    model = Comment
    readonly_fields = ["owner", "comment"]
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # just show their comments
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
        return ("poim", "owner", "comment")
