from django.urls import path
from .views import get_all_products, get_by_id_product, new_product, update_product, delete_product


urlpatterns = [
    path('products/', get_all_products),
    path('products/<str:pk>/', get_by_id_product, name='get_by_id_product'),
    path('products/new/', new_product, name='new_product'),
    path('products/update/<str:pk>/', update_product, name='update_product'),
    path('products/delete/<str:pk>/', delete_product, name='delete_product'),
]
