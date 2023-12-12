import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


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
    user = SignupSerializer(request.user, many=False)
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.user_name = data['user_name']
    user.email = data['email']

    if data['password'] != "":
        user.password = make_password(data['password'])

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(['POST'])
def forgot_pass(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now()+datetime.timedelta(minutes=40)
    user.profile.rest_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = "http://127.0.0.1:8000/api/reset_password/{token}".format(token=token)
    body = "your password reset link: {link}".format(link=link)
    send_mail(
        "password reset from eMarket",
        body,
        "er@er.com",
        [data['email']]
    )
    return Response({'details': 'password reset sent to {email}'.format(email=data['email'])})


@api_view(['POST'])
def reset_pass(request, token):
    data = request.data
    user = get_object_or_404(User, profile_reset_password_token=token)

    if user.profile_reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({"error": "Token is expired"}, status=status.HTTP_404_NOT_FOUND)

    if data['password'] != data['confirmPassword']:
        return Response({"error": "Password is unmatch"}, status=status.HTTP_404_NOT_FOUND)

    user.password = make_password(data['password'])
    user.profile.rest_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({"details": "password reset success"}, status=status.HTTP_201_CREATED)


