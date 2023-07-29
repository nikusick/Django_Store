import datetime

from rest_framework import serializers
from .models import Product, Tag, Specification, Review, Image, Category, SaleItem
from app_users.serializers import ProfileSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        depth = 2
        fields = ["id", "title", "image", "subcategories"]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullName")
    email = serializers.EmailField(source="author.user.email")

    class Meta:
        model = Review
        fields = ["text", "rate", "date", "author", "email", "product"]

    def create(self, validated_data):
        validated_data.pop("author")
        return Review.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        depth = 1
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]


class ProductShortSerializer(serializers.ModelSerializer):
    reviews = serializers.IntegerField(source="reviews.count")
    category = serializers.IntegerField(source="category.id")

    class Meta:
        model = Product
        depth = 1
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class SaleItemSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(source="product.price")
    title = serializers.CharField(source="product.title")
    images = ImageSerializer(source="product.images", many=True)

    class Meta:
        model = SaleItem
        depth = 1
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]
