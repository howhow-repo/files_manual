# # -*- encoding: utf-8 -*-
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
# from .models import Employee
#
#
# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#
#
# class AccountUserAdmin(BaseUserAdmin):
#     inlines = [EmployeeInline]
#
#
# admin.site.unregister(User)
# admin.site.register(User, AccountUserAdmin)
