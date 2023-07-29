from django.contrib import admin
from .models import Order, OrderProduct, OrderPriceConstants


class OrderPriceConstantsAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "value"


class OrderProductInline(admin.StackedInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = (
        "pk",
        "profile",
        "createdAt",
        "totalCost",
        "status",
        "address",
        "EXPRESS",
    )


class OrderProductAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "price", "count", "order"


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(OrderPriceConstants, OrderPriceConstantsAdmin)
