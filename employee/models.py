# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class BranchLocation(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100,  null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_location(cls):
        try:  # try catch to avoid error while makemigrations
            location, created = cls.objects.get_or_create(
                name='其他',
            )
            return location.pk
        except Exception:
            pass


class Department(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_department(cls):
        try:  # try catch to avoid error while makemigrations
            department, created = cls.objects.get_or_create(
                name='其他',
            )
            return department.pk
        except Exception:
            pass


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None,
                                   null=True)
    location = models.ForeignKey(BranchLocation, on_delete=models.CASCADE, default=None,
                                 blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    is_accept = models.BooleanField(default=True)
