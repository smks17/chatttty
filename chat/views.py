import datetime
from pytz import timezone
import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from chat.models import PromptModel, SessionModel, UserRole
from chatttty.settings import TIME_ZONE

from .forms import LoginForm, SignUpForm


import logging

logger = logging.getLogger("chat.views")


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
    form = SignUpForm(request.POST or None)
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
def chat(request):
    session_id = request.COOKIES.get("chat_session_id")
    query = SessionModel.objects.filter(user=request.user)
    if session_id:
        session = query.filter(session_id=session_id).first()
    else:
        session_name = f"session-{query.count()}"
        session = SessionModel(user=request.user, session_name=session_name)
        session.save()
        session_id = str(session.session_id)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception as exc:
            logger.error(f"Invalid message from {request.user.username} {request.body} cause {exc}")
            return JsonResponse({"error": "Invalid request"}, status=400)
        message = data.get("message", "").strip()
        if not message:
            logger.error(f"Message is None from {request.user.username}")
            return JsonResponse({"error": "Invalid request"}, status=400)
        session.updated_date = datetime.datetime.now(timezone(TIME_ZONE))
        user_prompt = PromptModel(role=UserRole.USER, content=message, session=session)
        user_prompt.save()
        logger.info(f"message from {request.user.username}: {message}")
        # TODO: create real message
        user_prompt = PromptModel(role=UserRole.ASSISTANCE, content=message, session=session)
        user_prompt.save()
        # TODO: return stream
        return JsonResponse({"sender": request.user.username, "message": message})
    elif request.method == "GET":
        messages = PromptModel.objects.filter(session=session).values("content", "role")
        return JsonResponse({
            "session_id": session_id,
            "session_name": session.session_name,
            "session_messages": list(messages)
        })
    return JsonResponse({"error": "Invalid request"}, status=405)


@login_required(login_url="/login/")
def sessions(request):
    # TODO: sort by updated date
    sessions = SessionModel.objects.filter(user=request.user).values("session_id", "session_name", "created_date").order_by("-updated_date", "-created_date")
    return JsonResponse({"sessions": list(sessions)})


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")
