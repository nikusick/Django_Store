from django.shortcuts import render

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from app_products.models import Product
from app_products.serializers import ProductShortSerializer
from .cart import Cart
from .models import OrderProduct, Order
from .serializers import OrderProductSerializer, OrderSerializer, PaymentSerializer
from app_users.models import Profile


class CartDetailView(APIView):
    """
    Представление о товарах в корзине
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            serializer = ProductShortSerializer(product)
            product_data = serializer.data
            product_data["count"] = item["quantity"]
            product_data["price"] = float(item["price"])
            cart_items.append(product_data)
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)


class OrdersView(APIView):
    """
    Представление о заказах пользователя
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        orders = Order.objects.filter(profile=profile)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.create(profile=profile)
        for item in request.data:
            product = Product.objects.get(id=item["id"])
            item_data = {"price": item["price"], "count": item["count"]}
            serializer = OrderProductSerializer(data=item_data, partial=True)
            if serializer.is_valid():
                serializer.save(product=product, order=order)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        return Response({"orderId": order.id})


class OrderDetailView(APIView):
    """Представление о заказе"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        order = Order.objects.get(id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        order = Order.objects.get(id=id)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            order.status = "ожидание оплаты"
            order.save()
            cart = Cart(request)
            cart.clear()
            return Response({"orderId": order.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    """Представление об оплате заказа"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = Order.objects.get(id=id)
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            order.status = "готов к получению"
            order.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
