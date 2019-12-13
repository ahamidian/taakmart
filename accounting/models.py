from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


# class User(AbstractUser):
#     username = models.CharField(
#         unique=True,
#         max_length=11,
#         validators=[RegexValidator('^09\d{9}$')],
#         help_text="Enter a valid 11 digit phone number starting with 09"
#     )
#     home_phone = models.CharField(max_length=11, validators=[RegexValidator('^0[1-8]\d{9}$')], null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)
#     verification_code = models.CharField(max_length=5, validators=[RegexValidator('^\d{5}$')], null=True, blank=True)
#     verification_code_created_on = models.DateTimeField(default=timezone.now)
#     last_sms_on = models.DateTimeField(null=True, blank=True)
#     is_verified = models.BooleanField(default=False)


class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    home_phone = models.CharField(max_length=11, validators=[RegexValidator('^0[1-8]\d{9}$')], null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    verification_code = models.CharField(max_length=5, validators=[RegexValidator('^\d{5}$')], null=True, blank=True)
    verification_code_created_on = models.DateTimeField(default=timezone.now)
    last_sms_on = models.DateTimeField(null=True, blank=True)


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
