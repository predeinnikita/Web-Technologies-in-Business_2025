# models.py

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="No Description")
    price = models.FloatField()
    image = models.ImageField(upload_to="productImages/", null=True, blank=True, default='productImages/not_available.png')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=100)
    unit_price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in order #{self.order.id}"

