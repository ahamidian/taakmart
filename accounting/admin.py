from django.contrib import admin
from django.contrib.admin import register
from accounting.models import User


@register(User)
class BrandAdmin(admin.ModelAdmin):
    pass
