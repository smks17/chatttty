import datetime
import json
import logging

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST
from pytz import timezone

from chat.functions import create_and_save_ai_response
from chat.forms import LoginForm, SignUpForm
from chat.models import PromptModel, SessionModel
from chatttty.settings import TIME_ZONE


logger = logging.getLogger("chat.views")


# TODO: User should choose any model and its settings
MODEL_NAME = "Mistral"


# TODO: Using class base views

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
@require_POST
def get_message(request):
    session_id = request.COOKIES.get("session_id")
    session = SessionModel.get_session_or_none(request.user, session_id, model_name=MODEL_NAME)
    if not session:
        return JsonResponse({"error": "Invalid request"}, status=400)
    try:
        data = json.loads(request.body)
    except Exception as exc:
        logger.error(
            f"Invalid message from {request.user.username} {request.body} cause {exc}"
        )
        return JsonResponse({"error": "Invalid request"}, status=400)
    message = data.get("message", "").strip()
    if not message:
        logger.error(f"Message is None from {request.user.username}")
        return JsonResponse({"error": "Invalid request"}, status=400)
    session.updated_date = datetime.datetime.now(timezone(TIME_ZONE))
    ai_response = create_and_save_ai_response(session, message, MODEL_NAME)
    logger.debug(f"message from {request.user.username}: {message}")
    logger.debug(f"And response: {ai_response}")
    # TODO: return stream
    return JsonResponse(
        {
            "sender": request.user.username,
            "session_id": session.session_id,
            "message": ai_response,
        }
    )


@login_required(login_url="/login")
@require_GET
def chat_history(request, session_id):
    # session_id = request.COOKIES.get("session_id")
    session = SessionModel.get_session_or_none(request.user, session_id, create_new=True, model_name=MODEL_NAME)
    response = JsonResponse({"session_messages": session.history})
    response.set_cookie("session_id", session.session_id, httponly=True, secure=True, samesite="Strict")
    return response


@login_required(login_url="/login")
@require_GET
def new_session(request):
    session = SessionModel.objects.create(user=request.user, model_name=MODEL_NAME)
    response = JsonResponse(session.dump())
    response.set_cookie("session_id", session.session_id, httponly=True, secure=True, samesite="Strict")
    return response


@login_required(login_url="/login/")
def sessions(request):
    sessions = (
        SessionModel.objects.filter(user=request.user)
        .values("session_id", "session_name", "created_date")
        .order_by("-updated_date", "-created_date")
    )
    return JsonResponse({"sessions": list(sessions)})


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")
