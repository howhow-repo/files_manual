# -*- encoding: utf-8 -*-
from django.db import models


class RecipeType(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_recipe_type(cls):
        try:  # try catch to avoid error while makemigrations
            recipe_type, created = cls.objects.get_or_create(
                name='其他',
            )
            return recipe_type.pk
        except Exception:
            pass


class Recipe(models.Model):
    name = models.CharField(max_length=20)
    type = models.ForeignKey(RecipeType, on_delete=models.CASCADE, default=None,null=True)
    picture = models.FileField(upload_to='Recipe')
    pdf = models.FileField(upload_to='Recipe')
    last_update = models.DateTimeField()
    description = models.CharField(max_length=100)


