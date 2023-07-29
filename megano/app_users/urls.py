from django.urls import path
from . import views

urlpatterns = [
    path("sign-in", views.SignInView.as_view(), name="login"),
    path("sign-up", views.SignUpView.as_view(), name="register"),
    path("sign-out", views.signOut, name="logout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/password", views.UpdatePasswordView.as_view(), name="update_password"
    ),
    path("profile/avatar", views.updateAvatar, name="update_avatar"),
]
