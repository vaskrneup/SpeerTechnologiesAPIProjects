from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from user.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Configuration for how the HTML will look in HTML page
    """

    fieldsets = (  # Placement for various field in the body.
        ("Main", {
            "fields": ("username", "password")
        }),
        ("Permissions", {
            "fields": (
                ("groups", "user_permissions"),
            )
        }),
        ("User Status", {
            "fields": (
                ("is_active", "is_staff", "is_superuser"),
            )
        }),
        ("Dates", {
            "fields": (
                ("last_login",),
            )
        }),
    )
    add_fieldsets = (  # For starting form, when the account is initially created!
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "is_staff")  # What field to display in list view of the data
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")  # What can be used to filter the data.
    search_fields = ("username",)  # What fields will be used when searching for data.
