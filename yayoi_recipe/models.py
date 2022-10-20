# -*- encoding: utf-8 -*-
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=20)
    picture = models.FileField(upload_to='Recipe')
    pdf = models.FileField(upload_to='Recipe')
    last_update = models.DateTimeField()
    description = models.CharField(max_length=100)
