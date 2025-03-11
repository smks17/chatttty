from chat.models import PromptModel, SessionModel, UserRole


def create_and_save_ai_response(session, message):
    user_prompt = PromptModel(role=UserRole.USER, content=message, session=session)
    user_prompt.save()
    # TODO: create real message
    ai_prompt = PromptModel(role=UserRole.ASSISTANCE, content=message, session=session)
    ai_prompt.save()
    return message
