from .models import Product, Review
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)

    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializer(product, many=False)
        return Response({"product": res.data})
    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({"error": "you cant update this product"},
                        status=status.HTTP_403_FORBIDDEN)
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_by_id_product(Product, id=pk)

    if product.user != request.user:
        return Response({"error": "sorry u cant delete this product"},
                        status=status.HTTP_403_FORBIDDEN)
    product.delete()
    return Response({"data": "deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    data = request.data
    review = product.reviews.filter(user=user)

    # if data['ratings'] <= 0 or >= 5 :
    #     return Response({"error": "please select valid review"}, status=status.HTTP_403_FORBIDDEN)
    #
    # elif review.exists():
    #     new_review = {'rating': data['rating'], 'comment': data['comment']}
    #     review.update(**new_review)
    #
    #     rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
    #     product,ratings = rating['avg_ratings']
    #     product.save()
    #
    #     return Response({"details": "Product review updated"})

    # else:
    #     Review.objects.create(
    #         user=user,
    #         product=product,
    #         rating=data['rating'],
    #         comment=data['comment']
    #     )
    #     rating = product.reviews.aggregate(avg_rating = Avg('rating'))
    #     product.ratings = rating['avg_ratings']
    #     product.save()
    #     return Response({"details": "Product review created"})



