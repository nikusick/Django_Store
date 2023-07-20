from django.urls import path
from . import views

urlpatterns = [
    # path('banners', views.banners),
    path('categories', views.CategoryView.as_view()),
    path('catalog', views.CatalogView.as_view()),
    # path('products/popular', views.productsPopular),
    path('products/limited', views.LimitedProductsView.as_view()),
    path('sales', views.SalesView.as_view()),
    path('product/<int:id>', views.ProductDetailAPIView.as_view()),
    path('product/<int:id>/reviews', views.ProductReview.as_view()),
    path('tags', views.TagsAPIView.as_view()),
]
