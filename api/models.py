from django.db import models
from rest_framework import generics,status
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

from .utils import unique_slug_generator

class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    imageUrl = models.ImageField(upload_to='api/static/images/categories', blank=True, null=True)
    class Meta:
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(
                name="unique_category_name_case_insensitive",
                fields=["name"],
                condition=None,
                violation_error_message="Category name must be unique (case-insensitive)",
            )
        ]
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    imageUrl = models.ImageField(upload_to='api/static/images/store_logos', blank=True, null=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)  # e.g. #FF5733
    def __str__(self):
        return self.name

class Product(models.Model):
    name               = models.CharField(max_length=30,null=False)
    description        = models.TextField()
    price              = models.DecimalField(max_digits=20,decimal_places=2)
    quantity           = models.IntegerField()
    category           = models.ForeignKey(Category,on_delete=models.CASCADE,default=None)
    discount           = models.IntegerField()
    date_added         = models.DateTimeField(auto_now_add=True)
    link               = models.SlugField(max_length=250,unique=True,null=True,blank=True)
    store              = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    colors             = models.ManyToManyField(Color, related_name='products', blank=True)
    def __str__(self):
        return f"{self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    imageUrl = models.ImageField(upload_to='api/static/images/products')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    def __str__(self):
        return f"Image for {self.product.name}"

class Banner(models.Model):
    title              = models.CharField(max_length=50,null=True,default="")
    description        = models.CharField(max_length=150,null=False)
    imageUrl              = models.ImageField(upload_to='api/static/images/banners')



def slug_generator(sender,instance,*args,**kwargs):
    if not instance.link:
        instance.link = unique_slug_generator(instance)



pre_save.connect(slug_generator,sender=Product)