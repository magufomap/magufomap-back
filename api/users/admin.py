from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UserChangeForm as DjangoUserChangeForm,
    UsernameField
)

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        field_classes = {"username": UsernameField}


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("full_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",
                                    "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "full_name", "is_staff")
    search_fields = ("username", "full_name", "email")
