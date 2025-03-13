import uuid
from django.contrib.auth.models import User
from django.db import models

from lib.llm import ModelsEnum
from lib.llm.base_llm import MessageInfo


class UserRole(models.TextChoices):
    SYSTEM = "system", "System"
    USER = "user", "User"
    ASSISTANCE = "assistant", "Assistant"


class SessionModel(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    session_name = models.CharField(max_length=50, null=True, default=None)
    user = models.ForeignKey(User, unique=False, default=None, null=False, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=20, choices=[(model.value, model.name) for model in ModelsEnum])

    def save(self, *args, **kwargs):
        if not self.session_name:
            count = SessionModel.objects.filter(user=self.user).count() + 1
            self.session_name = f"session-{count}"
        super().save(*args, **kwargs)

    @property
    def history(self):
        return [{"role": prompt.role.lower(), "content": prompt.content} for prompt in self.Prompt.all()]


    @classmethod
    def get_session_or_none(cls, user, session_id, create_new=True, model_name=""):
        session = None
        if not session_id:
            if create_new:
                return cls.objects.create(user=user, model_name=model_name)
        else:
            session = cls.objects.filter(user=user, session_id=session_id).first()
        return session


class PromptModel(models.Model):
    role = models.CharField(max_length=20, choices=UserRole.choices)
    content = models.TextField(blank=True, null=False)
    date = models.DateTimeField(auto_now=True)
    session = models.ForeignKey(
        SessionModel, on_delete=models.CASCADE, related_name="Prompt"
    )

    @property
    def llm_input(self) -> MessageInfo:
        return {
            "role": self.role.lower(),
            "content": self.content
        }
