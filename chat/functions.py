from chat.models import PromptModel, UserRole
from lib.llm import ModelsEnum
from lib.llm.base_llm import BaseLLM


def create_and_save_ai_response(session, message, model_name):
    user_prompt = PromptModel(role=UserRole.USER, content=message, session=session)
    user_prompt.save()
    model_api: BaseLLM = ModelsEnum[model_name].value
    model = model_api(chat_history=session.history)
    for chunk in model.get_response(user_prompt.llm_input):
        yield chunk + " "
    response = model.get_and_save_last_response()
    ai_prompt = PromptModel(role=UserRole.ASSISTANCE, content=response["content"], session=session)
    ai_prompt.save()
