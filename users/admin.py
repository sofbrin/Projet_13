from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class MyUserAdmin(UserAdmin):
    ordering = ['email']
    list_display = ('email', 'first_name', 'last_name', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Infos personnelles', {'fields': ('first_name', 'last_name')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
        ('Infos personnelles', {'fields': ('first_name', 'last_name')}),
    )


admin.site.register(User, MyUserAdmin)

