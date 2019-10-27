from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone


class Brand(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    url_code = models.CharField(max_length=255)
    queryString = models.CharField(max_length=255)
    is_leaf = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=CASCADE, null=True, blank=True)
    level = models.IntegerField(default=1)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Type(models.Model):
    title = models.CharField(max_length=255)
    search_value = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.CharField(max_length=255)
    existStatus = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=CASCADE)
    types = models.ManyToManyField(Type)
    parent = models.ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.title
