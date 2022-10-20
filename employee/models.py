# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


DEPARTMENT_CHOICES = (
    ('內場', '內場'),
    ('外場', '外場'),
    ('管理', '管理'),
    ('開發', '開發'),
    ('其他', '其他')
)


class BranchLocation(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100,  null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='其他')
    is_accept = models.BooleanField(default=False)
    location = models.ForeignKey(BranchLocation, on_delete=models.CASCADE, default=None, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
