from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('emart.urls')),
    path('api/', include('account.urls')),
    path('api/token/', TokenObtainPairView.as_view())
]

handler = 'utils.error_view.handler'
