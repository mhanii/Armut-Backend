from rest_framework import serializers
from django.contrib.auth.models import User
from user_profile.models import userProfile,userAddress
from .models import Verification





class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = "__all__"

class userAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = userAddress
        fields = "__all__"

class userVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['user', 'user_type']