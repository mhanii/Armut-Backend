from django.contrib import admin
from .models import userCartItem,userCart

# Register your models here.
@admin.register(userCart)
class Cart(admin.ModelAdmin):
    list_display=["user"]

@admin.register(userCartItem)
class CartItem(admin.ModelAdmin):
    list_display=["item"]
