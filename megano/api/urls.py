from django.urls import path
from . import views

urlpatterns = [
    path("banners", views.banners),
    path("categories", views.categories),
    path("catalog", views.catalog),
    path("products/popular", views.productsPopular),
    path("products/limited", views.productsLimited),
    path("sales", views.sales),
    path("basket", views.basket),
    path("orders", views.orders),
    path("sign-in", views.SignInView.as_view(), name="login"),
    path("sign-up", views.SignUpView.as_view(), name="register"),
    path("sign-out", views.signOut),
    path("product/<int:id>", views.product),
    path("product/<int:id>/reviews", views.productReviews),
    path("tags", views.tags),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/password", views.UpdatePasswordView.as_view(), name="update_password"
    ),
    path("profile/avatar", views.updateAvatar, name="update_avatar"),
    path("order/<int:id>", views.order),
    path("payment/<int:id>", views.payment),
]
