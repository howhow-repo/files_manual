# -*- encoding: utf-8 -*-
import os
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    megabyte_limit = 1.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def update_img(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Recipe/img/%s.%s' % (filename_, file_extension)


def update_doc(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Recipe/doc/%s.%s' % (filename_, file_extension)


class RecipeType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=20, unique=True)
    type = models.ForeignKey(RecipeType, on_delete=models.PROTECT, default=None, null=True)
    cover = models.ImageField(upload_to=update_img, validators=[validate_image])
    pdf = models.FileField(upload_to=update_doc, validators=[validate_file_extension])
    last_update = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100, null=True, blank=True)
