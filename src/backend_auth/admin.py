from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core import models as cm

from . import models as am


class BookInline(admin.TabularInline):
    model = cm.Book

    fk_name = "writer"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)


class BackendUserAdmin(UserAdmin):

    inlines = [BookInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        *UserAdmin.fieldsets[1:],
    )
    list_display = UserAdmin.list_display

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else qs.filter(is_superuser=False)


admin.site.register(am.BackendUser, BackendUserAdmin)
