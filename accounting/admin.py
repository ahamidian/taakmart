from django.contrib import admin
from django.contrib.admin import register
from accounting.models import User, Seller, Company


@register(User)
class BrandAdmin(admin.ModelAdmin):
    pass


@register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass


@register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
