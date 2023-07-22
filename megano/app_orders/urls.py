from django.urls import path
from . import views

urlpatterns = [
    path('basket', views.CartDetailView.as_view()),
    # path('orders', views.orders),
    # path('order/<int:id>', views.order),
    # path('payment/<int:id>', views.payment),
]
