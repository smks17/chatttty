import os
import sys
from typing import List, Optional, Union

sys.path.append(".")

from mistralai import Dict, Mistral

from lib.llm.base_llm import BaseLLM, MessageInfo

api_key = os.environ.get("MISTRAL_API_KEY")
model = "mistral-large-latest"


class MistralAPI(BaseLLM):
    LLM_NAME = "Mistral"

    def __init__(self, model: str="mistral-large-latest", chat_history: Optional[List[MessageInfo]]=None, settings: Optional[Dict]=None) -> None:
        self.model = model
        self.client = Mistral(api_key=api_key)
        self.chat_history: List[MessageInfo] = chat_history or []
        self.settings = settings or {}

    def get_response(self, message: MessageInfo) -> MessageInfo:
        self._add_new_prompt(message)
        chat_response = self.client.chat.complete(
            model= model,
            messages = self.chat_history,
            **self.settings
        )
        ai_response = chat_response.choices[0].message
        ai_response = {"role": ai_response.role, "content": ai_response.content}
        self._add_new_prompt(ai_response)
        return ai_response

    def _add_new_prompt(self, new_prompt: MessageInfo) -> None:
        self.chat_history.append(new_prompt)
