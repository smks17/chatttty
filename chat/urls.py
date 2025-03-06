from django.urls import path

from .views import login_view, signup_view, logout_view, index


urlpatterns = [
    path("", index),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
]
