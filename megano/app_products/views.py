import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer, ReviewSerializer


class ProductDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)


class ProductReview(APIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        product = Product.objects.get(id=id)
        data = request.data
        data.update({'product': product})
        serializer = ReviewSerializer(data=data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
