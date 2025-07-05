from rest_framework import serializers
from .models import userProfile,userAddress, Order, OrderItem
from api.serializer import ProductTypeSerializer



class UserProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model               =   userProfile
        fields              =   "__all__"


class UserProfileAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model               =   userAddress
        fields              =   "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductTypeSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'created_at', 'shipping_address', 'items']

