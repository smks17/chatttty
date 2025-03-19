import sys
from typing import Generator

sys.path.append(".")

from lib.llm.base_llm import BaseLLM, MessageInfo


class EchoAPI(BaseLLM):
    """This class is just for better and faster debug"""
    LLM_NAME = "Echo"

    def __init__(self, **kwargs) -> None:
        self.f = lambda x: x["content"].split()
        self.last_response = ""

    def get_response(self, message: MessageInfo) -> Generator:
        chat_response = self.f(message)
        self.last_response = ""
        for chunk in chat_response:
            self.last_response += chunk
            yield chunk

    def get_and_save_last_response(self) -> MessageInfo:
        ai_response = {"role": "Assistant", "content": self.last_response}
        self._add_new_prompt(ai_response)
        return ai_response

    def _add_new_prompt(self, new_prompt: MessageInfo) -> None:
        pass