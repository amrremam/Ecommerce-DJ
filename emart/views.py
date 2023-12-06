from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.shortcuts import render, get_object_or_404
from .filters import ProductFilter


@api_view(['GET'])
def get_all_products(request):
    # products = Product.objects.all()
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    serializer = ProductSerializer(filterset.qs, many=True)
    return Response({"products": serializer.data})


@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})
