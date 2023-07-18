from django.urls import path
from . import views

urlpatterns = [
    # path('banners', views.banners),
    # path('categories', views.categories),
    # path('catalog', views.catalog),
    # path('products/popular', views.productsPopular),
    # path('products/limited', views.productsLimited),
    # path('sales', views.sales),
    path('product/<int:id>', views.ProductDetailAPIView.as_view()),
    path('product/<int:id>/reviews', views.ProductReview.as_view()),
    # path('tags', views.tags),
]
