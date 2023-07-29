from django.contrib import admin
from .models import Image, Category, Tag, Specification, Product, Review, SaleItem


class ImageAdmin(admin.ModelAdmin):
    list_display = "pk", "src", "alt"


class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "image", "parent_category"


class TagAdmin(admin.ModelAdmin):
    def get_products(self, tag):
        return [product.title for product in tag.products.all()]

    get_products.short_description = "Товары с тэгом"
    list_display = "name", "get_products"


class SpecificationAdmin(admin.ModelAdmin):
    list_display = "name", "value"


class ProductAdmin(admin.ModelAdmin):
    list_display = "title", "price", "category", "rating"


class ReviewAdmin(admin.ModelAdmin):
    list_display = "author", "text", "rate", "date"


class SaleItemAdmin(admin.ModelAdmin):
    def old_price(self, item):
        return item.product.price

    old_price.short_description = "Старая цена"
    list_display = "product", "old_price", "salePrice"


admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
