from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE, Max
from django.utils import timezone
from ordered_model.models import OrderedModel

from accounting.models import Company


class Brand(models.Model):
    title = models.CharField(max_length=255)
    fa_title = models.CharField(max_length=255,null=True,blank=True)
    image = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    url_code = models.CharField(max_length=255, null=True, blank=True)
    queryString = models.CharField(max_length=255, null=True, blank=True)
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
    created_on = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Slide(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255)
    internal_link = models.CharField(max_length=255, null=True, blank=True)
    external_link = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class HomepageSegment(OrderedModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    query = models.CharField(max_length=255, null=True, blank=True)
    products = models.ManyToManyField(Product, null=True, blank=True)
    external_link = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
