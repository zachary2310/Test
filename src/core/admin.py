from admin_numeric_filter.admin import NumericFilterModelAdmin
from django.contrib import admin

from . import models as cm


class BookAdmin(NumericFilterModelAdmin):
    # list_filter = (ExpiredFilter,)
    list_display = [
        "writer",
        "name",
        "genre",
        "price",
    ]
    search_fields = [
        "genre",
        "writer",
    ]


admin.site.register(cm.Book, BookAdmin)
admin.site.register(cm.BookGenre)
