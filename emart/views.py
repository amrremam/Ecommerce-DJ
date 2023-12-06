from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.shortcuts import render, get_object_or_404
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def get_all_products(request):
    filter_set = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filter_set.qs.count()
    page_size = 2
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    serializer = ProductSerializer(filter_set.qs, many=True)
    return Response({"products": serializer.data, "per page": page_size, "count": count})


@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})
