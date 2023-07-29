import datetime
import json
from collections import OrderedDict

from django.db.models import Count, QuerySet
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Tag, SaleItem
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    TagSerializer,
    CategorySerializer,
    ProductShortSerializer,
    SaleItemSerializer,
)
from app_users.models import Profile


class TagsAPIView(APIView):
    """
    Представление тэгов
    """

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProductDetailAPIView(APIView):
    """
    Детальное представление товара
    """

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductReview(APIView):
    """
    Представление для добавления отзыва на товар
    """

    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        data = request.data
        serializer = ReviewSerializer(data=data, partial=True)
        if serializer.is_valid():
            profile = Profile.objects.get(user=request.user)
            serializer.save(author_id=profile.id, product_id=id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    """
    Представление категорий
    """

    def get(self, request):
        categories = Category.objects.filter(parent_category__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)


class CatalogView(APIView):
    """
    Представление каталога
    """

    def get(self, request):
        r = request.GET
        name = r.get("filter[name]")
        minPrice = int(r.get("filter[minPrice]"))
        maxPrice = int(r.get("filter[maxPrice]"))
        freeDelivery = json.loads(r.get("filter[freeDelivery]").lower())
        available = json.loads(r.get("filter[available]").lower())
        currentPage = int(r.get("currentPage"))
        category = int(r.get("category", -1))
        sort = f'{"-" if r.get("sortType") == "dec" else ""}{r.get("sort")}'
        tags = Tag.objects.filter(id__in=map(int, dict(r).get("tags[]", [])))
        limit = int(r.get("limit"))

        products = Product.get_category_items(category_id=category)

        if len(tags) != 0:
            products = products.filter(
                tags__in=tags,
            )
        products = products.filter(
            title__icontains=name,
            price__range=[minPrice, maxPrice],
            freeDelivery__gte=1 if freeDelivery else 0,
            count__gte=1 if available else 0,
        ).order_by(sort)[:limit]
        serializer = ProductShortSerializer(
            list(OrderedDict.fromkeys(products)), many=True
        )
        data = {"items": serializer.data, "currentPage": currentPage, "lastPage": 10}
        return Response(data, status=status.HTTP_200_OK)


class LimitedProductsView(APIView):
    """
    Представление товаров ограниченного тиража
    """

    def get(self, request):
        products = Product.objects.filter(limited=True)[:16]
        serializer = ProductShortSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularProductsView(APIView):
    """
    Представление популярных товаров
    """

    def get(self, request):
        products = Product.objects.order_by("rating")[:8]
        serializer = ProductShortSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesView(APIView):
    """
    Представление акционных товаров
    """

    def get(self, request):
        saleItems = SaleItem.objects.filter(
            dateFrom__lte=datetime.datetime.now().date(),
            dateTo__gte=datetime.datetime.now().date(),
        )
        serializer = SaleItemSerializer(saleItems, many=True)
        data = {
            "items": serializer.data,
            "currentPage": int(request.GET.get("currentPage")),
            "lastPage": 10,
        }
        return Response(data, status=status.HTTP_200_OK)


class BannerView(APIView):
    """
    Представление рекламы
    """

    def get(self, request):
        products = Product.objects.filter(on_banner=True)
        serializer = ProductShortSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
