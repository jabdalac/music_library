from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import password_validation, get_user_model
from .models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
    def get_auth_token(self, obj):
        user = get_user_model().objects.filter(pk=obj.pk).first()
        token = Token.objects.get(user=user)
        return token.key

class RegisterSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = (
            'id', 
            'email', 
            'name', 
            'country', 
            'auth_token',
            'is_active', 
            'is_staff',
            'is_superuser'
        )
         read_only_fields = ('id', 'is_active', 'auth_token', '')
    
    def get_auth_token(self, obj):
        user = get_user_model().objects.filter(pk=obj.pk).first()
        token = Token.objects.create(user=user)
        return token.key

    def validate_email(self, value):
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value