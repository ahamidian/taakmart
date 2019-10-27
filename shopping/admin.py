from django.contrib import admin
from django.contrib.admin import register

from shopping.models import Order, OrderLine


@register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    pass
