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
        location, created = cls.objects.get_or_create(
            name='其他',
        )
        return location.pk


class Department(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_department(cls):
        department, created = cls.objects.get_or_create(
            name='其他',
        )
        return department.pk


Department.objects.get_or_create(
    name='開發'
)[0].save()


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=Department.get_default_department(),
                                   null=True)
    is_accept = models.BooleanField(default=False)
    location = models.ForeignKey(BranchLocation, on_delete=models.CASCADE, default=BranchLocation.get_default_location(),
                                 blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
