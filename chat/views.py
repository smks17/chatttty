from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, SignUpForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = LoginForm(request, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user_data = form.get_user()
            login(request, user_data)
            return redirect("/")
    return render(request, "auth/login.html", {"form": form})


def signup_view(request):
    form = SignUpForm(request, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("/")
    return render(request, "auth/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")
