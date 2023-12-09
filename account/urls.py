from django.urls import path
from .views import register, current_user


url_patterns = [
    path('register/', register, name='register'),
    path('user_details/', current_user, name='current_user')
]