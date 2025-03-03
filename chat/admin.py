from django.contrib import admin

from .models import SessionModel, PromptModel

admin.site.register(SessionModel)
admin.site.register(PromptModel)
