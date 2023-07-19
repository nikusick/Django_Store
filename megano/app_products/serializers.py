import datetime

from rest_framework import serializers
from .models import Product, Tag, Specification, Review, Image, Category
from app_users.serializers import ProfileSerializer


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        depth = 2
        fields = '__all__'


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
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id", "category", "price", "count", "date", "title",
            "description", "fullDescription", "freeDelivery",
            "images", "tags", "reviews", "specifications", "rating"
        ]
