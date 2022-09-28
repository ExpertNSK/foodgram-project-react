from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email',
        'first_name', 'last_name', 'role',
    )
    search_fields = (
        'username', 'first_name', 'last_name', 'email',
    )
    list_filter = (
        'role',
    )
    list_editable = ('role',)
    empty_value_display = '---none---'


admin.site.register(User, UserAdmin)
