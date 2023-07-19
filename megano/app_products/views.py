import datetime
import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category
from .serializers import ProductSerializer, ReviewSerializer, TagSerializer, CategorySerializer
from app_users.models import Profile


class TagsListAPIView(APIView):

    def get(self, request):
        tags = TagSerializer(many=True)
        print(tags)


class ProductDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductReview(APIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        data = request.data
        serializer = ReviewSerializer(data=data, partial=True)
        if serializer.is_valid():
            profile = Profile.objects.get(user=request.user)
            serializer.save(author_id=profile.id, product_id=id,
                            date=datetime.datetime.now(tz=datetime.timezone.utc))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
