from django.contrib import admin
from .models import RecipeType, Recipe


class RecipeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'picture', 'pdf', 'last_update', 'description')


admin.site.register(RecipeType, RecipeTypeAdmin)
admin.site.register(Recipe, RecipeAdmin)
