from __future__ import unicode_literals

from django.db import models


# Create your models here.
class user_data(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.BigIntegerField(blank=False, null=False, max_length=10,)
    password = models.CharField(null=False, blank=False, max_length=20)


class user_otp(models.Model):
    mobile = models.BigIntegerField(blank=False, null=False, max_length=10,)
    otp = models.IntegerField(blank=False, null=False)
