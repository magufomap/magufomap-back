from django import forms
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from api.models import POI, POIImage, Rating, Comment, Visited, ChangeRequest
from mapwidgets.widgets import GooglePointFieldWidget


class ImageInline(admin.TabularInline):
    model = POIImage


class RatingAdmin(admin.ModelAdmin):
    model = Rating

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # si no es superuser, no puede editar los comentarios
        return ('poi', 'user', 'vote')


class RatingEditorInline(admin.TabularInline):
    model = Rating
    readonly_fields = ['user', 'poi', 'vote']


class RatingInline(admin.TabularInline):
    model = Rating


class CommentEditorInline(admin.TabularInline):
    model = Comment
    readonly_fields = ['user', 'comment']


class CommentInline(admin.TabularInline):
    model = Comment


class CommentAdmin(admin.ModelAdmin):
    model = Comment

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # si no es superuser, no puede editar los comentarios
        return ('poi', 'user', 'comment')


class ChangeRequestEditorInline(admin.TabularInline):
    model = ChangeRequest
    readonly_fields = ['user', 'change']


class ChangeRequestInline(admin.TabularInline):
    model = ChangeRequest


class ChangeRequestAdmin(admin.ModelAdmin):
    model = ChangeRequest

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # si no es superuser, no puede editar los comentarios
        return ('poi', 'user', 'change')


class VisitedEditorInline(admin.TabularInline):
    model = Visited
    readonly_fields = ['user', 'visited']


class VisitedInline(admin.TabularInline):
    model = Visited


class VisitedAdmin(admin.ModelAdmin):
    model = Visited

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # si no es superuser, no puede editar los comentarios
        return ('poi', 'user', 'visited')


class POIAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    inlines = [
            ImageInline,
    ]
    admin_inlines = [
            ChangeRequestInline,
            RatingInline,
            CommentInline,
            VisitedInline
    ]
    editor_inlines = [
            ChangeRequestEditorInline,
            RatingEditorInline,
            CommentEditorInline,
            VisitedEditorInline
    ]

    def get_inline_instances(self, request, obj):
        if request.user.is_superuser:
            inlines = self.inlines + self.admin_inlines
            return [inline(self.model, self.admin_site) for inline in inlines]

        # si no es superuser, no puede editar los comentarios
        inlines = self.inlines + self.editor_inlines
        return [inline(self.model, self.admin_site) for inline in inlines]


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form

        # si no es superuser, solo puede ponerse a sí misma como autora
        form.base_fields['author'].queryset = User.objects.filter(pk=request.user.id)
        return form


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # si no es superuser, solo puede ver los pois de los que es author
        return super().get_queryset(request).filter(author=request.user)


admin.site.register(POI, POIAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Visited, VisitedAdmin)
admin.site.register(ChangeRequest, ChangeRequestAdmin)
