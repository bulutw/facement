from rest_framework import serializers
from .models import MobileUser

class MobileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileUser
        fields = ['username', 'password']