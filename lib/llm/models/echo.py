import sys

sys.path.append(".")

from lib.llm.base_llm import BaseLLM, MessageInfo


class EchoAPI(BaseLLM):
    """This class is just for better and faster debug"""
    LLM_NAME = "Echo"

    def __init__(self, **kwargs) -> None:
        self.f = lambda x: x["content"]

    def get_response(self, message: MessageInfo) -> MessageInfo:
        chat_response = self.f(message)
        chat_response = {"role": "Assistant", "content": chat_response}
        return chat_response

    def _add_new_prompt(self, new_prompt: MessageInfo) -> None:
        pass