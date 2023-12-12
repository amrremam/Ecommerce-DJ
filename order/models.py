from django.db import models
from operator import mod
from django.contrib.auth.models import User
from emart.models import Product


class OrderStatus(models.TextChoices):
    PROCESSING = 'processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'


class Payment(models.TextChoices):
    COD = 'Cod'
    CARD = 'Card'


class Order(models.Model):
    city = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    total = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=30, choices=OrderStatus.choices, default=Payment.UNPAID)
    payment_mode = models.CharField(max_length=30, choices=Payment.choices, default=Payment.COD)
    status = models.CharField(max_length=60, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='orderItems')
    name = models.CharField(max_length=300, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __str__(self):
        return str(self.id)
