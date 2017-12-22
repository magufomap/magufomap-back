from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as geomodels
from api.models import (POI, POIImage,
                        Rating, Comment,
                        Visited, ChangeRequest)
from mapwidgets.widgets import GooglePointFieldWidget


class ImageInline(admin.TabularInline):
    model = POIImage


class RatingAdmin(admin.ModelAdmin):
    model = Rating

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # si no es superuser, solo puede ver los ratings que ha hecho
        return super().get_queryset(request).filter(user=request.user)


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

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # si no es superuser, solo puede ver los comments que ha hecho
        return super().get_queryset(request).filter(user=request.user)


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

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # si no es superuser, solo puede ver los change request que ha hecho
        return super().get_queryset(request).filter(user=request.user)


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

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        # si no es superuser, solo puede ver los pois de los que es author
        return super().get_queryset(request).filter(author=request.user)


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
    exclude = ['author']

    def get_inline_instances(self, request, obj):
        if request.user.is_superuser:
            inlines = self.inlines + self.admin_inlines
            return [inline(self.model, self.admin_site) for inline in inlines]

        # si no es superuser, no puede editar los comentarios
        inlines = self.inlines + self.editor_inlines
        return [inline(self.model, self.admin_site) for inline in inlines]

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


# def create_modeladmin(modeladmin, model, name=None):
#     class  Meta:
#         proxy = True
#         app_label = 'api'
#         permissions = (
#             ('can_myrating_add', 'Can add myrating'),
#         )
#
#     attrs = {'__module__': 'api.models', 'Meta': Meta}
#     newmodel = type(name, (model,), attrs)
#
#     content_type = ContentType.objects.get(app_label='api', model=name.lower())
#     perms = Permission.objects.filter(content_type=content_type)
#     group = Group.objects.get(name='Editor')
#     for p in perms:
#         group.permissions.add(perms)
#
#     admin.site.register(newmodel, modeladmin)
#     return modeladmin
#
#
# class MyRating(Rating):
#     class Meta:
#         proxy = True
#         app_label = 'api'
#         permissions = (
#             ('add_myrating', 'Can add myrating'),
#         )
#
#
# class MyRatingAdmin(RatingAdmin):
#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return super().get_queryset(request)
#
#         # si no es superuser, solo puede ver los ratings que le han hecho a sus pois
#         return super().get_queryset(request).filter(poi__author=request.user)
#
# content_type = ContentType.objects.get(app_label='api', model='myrating')
# import pdb; pdb.set_trace()
# admin.site.register(MyRating, MyRatingAdmin)
# create_modeladmin(MyRatingAdmin, name='MyRating', model=Rating)
