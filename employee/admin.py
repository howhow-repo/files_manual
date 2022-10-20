# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'department', 'phone_number', 'is_accept')
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Additional Info',
            {
                'fields': (
                    'nickname',
                    'department',
                    'is_accept'
                )
            }
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )


admin.site.register(User, CustomUserAdmin)