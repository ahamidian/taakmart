from django.db import models
from django.db.models import CASCADE
from django.utils import timezone

from accounting.models import User, Seller
from main.models import Product


class Order(models.Model):
    STATUS_DRAFT = 0
    STATUS_USER_ACCEPT = 1
    STATUS_ACCEPTED = 2
    STATUS_PAID = 3
    STATUS_SENT = 4
    STATUS_CANCELED = 5
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Draft"),
        (STATUS_USER_ACCEPT, "User accepted"),
        (STATUS_ACCEPTED, "Admin accepted"),
        (STATUS_PAID, "Paid"),
        (STATUS_SENT, "Sent"),
        (STATUS_CANCELED, "Canceled"),
    )
    STATUSES = {k: v for (k, v) in STATUS_CHOICES}

    owner = models.ForeignKey(Seller, null=True, blank=True, on_delete=CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)
    description = models.TextField(null=True, blank=True)
    code = models.IntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # def get_sum(self):
    #     price = 0
    #     for order_stuff in self.order_set.all():
    #         price += order_stuff.price
    #     return price


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE,related_name="lines")
    product = models.ForeignKey(Product, on_delete=CASCADE)
    amount = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
