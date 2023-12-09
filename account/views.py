from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignupSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignupSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password']),
            )
            return Response({'details': 'Success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'this mail already exist'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = SignupSerializer(request.user)
    return Response(user.data)
