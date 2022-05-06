from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from .serializers import GetTokenSerializer

@api_view(['POST'])
def login(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        access_token = RefreshToken.for_user(user).access_token
        data = {"token": str(access_token)}
        return Response(data, status=status.HTTP_201_CREATED)
    errors = {"error": "email or password is incorrect"}
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)



