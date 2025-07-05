from django.contrib import admin
from .models import userAddress, Order, OrderItem


@admin.register(userAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display=["user","address_1"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total", "created_at"]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price"]


