from rest_framework import serializers
from .models import userCart


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model               =   userCart
        fields              =   "__all__"