import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.mp4', '.mov']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def update_img(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Precaution/img/%s.%s' % (filename_, file_extension)


def update_doc(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    if file_extension.lower() in ['mp4', 'mov']:
        return settings.DOCS_ROOT + '/Precaution/video/%s.%s' % (filename_, file_extension)
    elif file_extension == 'pdf':
        return settings.DOCS_ROOT + '/Precaution/doc/%s.%s' % (filename_, file_extension)


class PrecautionType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name


class Precaution(models.Model):
    name = models.CharField(max_length=10, unique=True)
    type = models.ForeignKey(PrecautionType, on_delete=models.PROTECT, default=None, null=True)
    cover = models.ImageField(upload_to=update_img, null=True, blank=True, validators=[validate_image])
    doc_type = models.CharField(max_length=10,null=True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    file = models.FileField(upload_to=update_doc, null=True, blank=True, validators=[validate_file_extension])
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
