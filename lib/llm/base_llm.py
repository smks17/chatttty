from typing import List, TypedDict
from abc import ABC, abstractclassmethod


class MessageInfo(TypedDict):
    role: str
    content: str


class BaseLLM(ABC):
    LLM_NAME = ""

    @abstractclassmethod
    def get_response(self, prompt: str) -> str: ...

    @abstractclassmethod
    def _add_new_prompt(self, new_prompt: MessageInfo) -> None:...
