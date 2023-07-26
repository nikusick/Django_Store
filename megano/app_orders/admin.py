from django.contrib import admin
from .models import Order, OrderProduct, Payment


class OrderProductInline(admin.StackedInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = 'pk', 'profile', 'createdAt', 'totalCost', 'status', 'address'


class OrderProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'product', 'price', 'count', 'order'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
