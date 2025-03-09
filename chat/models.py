import uuid
from django.contrib.auth.models import User
from django.db import models


class UserRole(models.TextChoices):
    SYSTEM = "system", "System"
    USER = "user", "User"
    ASSISTANCE = "assistance", "Assistance"


class SessionModel(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    session_name = models.CharField(max_length=50, null=True, default=None)
    user = models.ForeignKey(User, unique=False, default=None, null=False, on_delete=models.CASCADE)


class PromptModel(models.Model):
    role = models.CharField(max_length=20, choices=UserRole.choices)
    content = models.TextField(blank=True, null=False)
    date = models.DateTimeField(auto_now=True)
    session = models.ForeignKey(
        SessionModel, on_delete=models.CASCADE, related_name="Prompt"
    )
