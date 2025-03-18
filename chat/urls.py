from django.urls import path

from .views import login_view, signup_view, logout_view, index, sessions, chat_history, get_message, new_session


urlpatterns = [
    path("", index),
    path("session/<str:session_id>", chat_history),
    path("chat/", get_message),
    path("create-session/", new_session),
    path("sessions/", sessions),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
]
