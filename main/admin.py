from django.contrib import admin
from django.contrib.admin import register

from main.models import Category, Brand, Product, Type, Slide, HomepagePhoto, Collection


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


@register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['title', "image", "internal_link", "external_link", "created_on", "is_active"]


@register(HomepagePhoto)
class HomepagePhotoAdmin(admin.ModelAdmin):
    list_display = ['title', "image", "internal_link", "external_link", "created_on", "is_active"]


@register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', "query", "created_on", "is_active"]
