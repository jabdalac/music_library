from rest_framework import generics
from django.contrib.auth import authenticate,logout
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)

class Login(generics.CreateAPIView):
    """
    CreateAPIView Login.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(username=request.data["email"], password=request.data["password"])
        try:
            if user is None:
                raise serializers.ValidationError("Invalid email or password")
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)


class Register(generics.CreateAPIView):
    """
    CreateAPIView Register.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            email = request.data.get("email", None)
            if not email:
                raise serializers.ValidationError("Please specify an email")
            user_check = User.objects.filter(email=email)
            if user_check:
                raise serializers.ValidationError("Email already registered")
            user = User.objects.create_user(**request.data)
            data = RegisterSerializer(user).data
            return Response(data=data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
    APIView Logout.
    """
    def post(self, request):
        try:
            logout(request)
            data = {'success': 'Sucessfully logged out'}
            return Response(data=data, status = HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, HTTP_400_BAD_REQUEST)