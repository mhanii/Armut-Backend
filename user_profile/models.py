from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from api.models import Product
from django.contrib.auth.models import AbstractUser, Group, Permission



class userProfile(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=50,default='')
    last_name       = models.CharField(max_length=50,default='')
    phone_number    = PhoneField(blank=True,help_text="Contact phone number")
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    

class userAddress(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    title           = models.CharField(max_length=50,default='')
    town            = models.CharField(max_length=20,default='')
    area            = models.CharField(max_length=30,default='')
    road            = models.CharField(max_length=50,default='')
    building        = models.CharField(max_length=50,default='')
    floor           = models.IntegerField(blank=True, null=True)
    door_number     = models.IntegerField(blank=True, null=True)
    address_1       = models.CharField(max_length=150,default='')
    def __str__(self):
        return f"{self.user.username}'s  {self.title} - Address"

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey('userAddress', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def get_vendor_orders(vendor):
        return OrderItem.objects.filter(product__store__owner=vendor)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

