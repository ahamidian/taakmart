from django.contrib import admin
from django.contrib.admin import register

from main.models import Category, Brand, Product, Type


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', "parent", "queryString", "is_leaf"]
    ordering = ["level", "parent"]


@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title']


@register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', "parent", "brand", "existStatus"]


@register(Type)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
