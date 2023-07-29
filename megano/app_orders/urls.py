from django.urls import path
from . import views

urlpatterns = [
    path("basket", views.CartDetailView.as_view()),
    path("orders", views.OrdersView.as_view()),
    path("order/<int:id>", views.OrderDetailView.as_view()),
    path("payment/<int:id>", views.PaymentView.as_view()),
]
