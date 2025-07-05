from django.db import models
from user_profile.models import User
from api.models import Product

# Create your models here.
class userCartItem(models.Model):
    cart = models.ForeignKey('userCart', on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cart.user.username} - {self.quantity} x {self.item.name}"

class userCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(userCartItem)

    def __str__(self):
        return self.user.username + "'s Cart"



