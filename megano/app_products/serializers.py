import datetime

from rest_framework import serializers
from .models import Product, Tag, Specification, Review, Image, Category
from app_users.serializers import ProfileSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        depth = 2
        fields = ['id', 'title', 'image', 'subcategories']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.fullName')
    email = serializers.EmailField(source='author.user.email')

    class Meta:
        model = Review
        fields = ['text', 'rate', 'date', 'author', 'email', 'product']

    def create(self, validated_data):
        validated_data.pop('author')
        return Review.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        depth = 1
        fields = [
            "id", "category", "price", "count", "date", "title",
            "description", "fullDescription", "freeDelivery",
            "images", "tags", "reviews", "specifications", "rating"
        ]


class ProductShortSerializer(serializers.ModelSerializer):
    reviews = serializers.IntegerField(source='reviews.count')

    class Meta:
        model = Product
        depth = 1
        fields = [
            "id", "category", "price", "count", "date", "title",
            "description", "freeDelivery",
            "images", "tags", "reviews", "rating"
        ]