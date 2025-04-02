import os
import sys
from typing import Generator, List, Optional

sys.path.append(".")

from mistralai import Dict, Mistral

from lib.llm.base_llm import BaseLLM, MessageInfo

api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"


class MistralAPI(BaseLLM):
    LLM_NAME = "Mistral"

    def __init__(self, model: str="mistral-large-latest", chat_history: Optional[List[MessageInfo]]=None, settings: Optional[Dict]=None) -> None:
        self.model = model
        self.client = Mistral(api_key=api_key)
        self.chat_history: List[MessageInfo] = chat_history or []
        self.settings = settings or {}
        self.last_response = ""

    def get_response(self, message: MessageInfo) -> Generator:
        self._add_new_prompt(message)
        self.last_response = ""
        for chunk_response in self.client.chat.stream(
            model= model,
            messages = self.chat_history,
            stream=True,
            **self.settings
        ):
            if chunk_response == "[DONE]":
                break
            chunk = chunk_response.data.choices[0].delta.content
            if not chunk:
                continue
            self.last_response += chunk
            yield chunk

    def get_and_save_last_response(self) -> MessageInfo:
        ai_response = {"role": "Assistant", "content": self.last_response}
        self._add_new_prompt(ai_response)
        return ai_response

    def _add_new_prompt(self, new_prompt: MessageInfo) -> None:
        self.chat_history.append(new_prompt)
