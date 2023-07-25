from rest_framework import serializers

from .models import OrderProduct, Order, Payment

from app_products.serializers import ProductShortSerializer

from app_products.models import Product


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        depth = 1
        fields = ['id', 'product', 'price', 'count', 'order']


class OrderSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source='profile.fullName')
    email = serializers.EmailField(source='profile.user.email')
    phone = serializers.CharField(source='profile.phone')
    totalCost = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        products = []
        for cur_product in representation.get('products'):
            product = cur_product.get('product')
            product['price'] = float(product['price'])
            product['count'] = cur_product['count']
            products.append(product)
        representation['products'] = products
        return representation

    def get_totalCost(self, obj):
        return obj.get_total_cost()

    class Meta:
        model = Order
        depth = 3
        fields = ["id", "createdAt", "fullName", "email", "phone",
                  "deliveryType", "paymentType", "totalCost", "status",
                  "city", "address", "products"]

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone')
        instance.deliveryType = validated_data.get('deliveryType')
        instance.paymentType = validated_data.get('paymentType')
        instance.totalCost = instance.get_total_cost()
        instance.status = validated_data.get('status')
        instance.city = validated_data.get('city')
        instance.address = validated_data.get('address')
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
