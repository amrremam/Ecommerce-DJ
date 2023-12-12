from django.urls import path
from .views import register, current_user, update_user, forgot_pass, reset_pass

urlpatterns = [
    path('register/', register, name='register'),
    path('user_details/', current_user, name='current_user'),
    path('user_info/update/', update_user, name='update'),
    path('forget_pass/', forgot_pass, name='forget_pass'),
    path('reset_pass/<str:token>/', reset_pass, name='reset_pass'),
]
