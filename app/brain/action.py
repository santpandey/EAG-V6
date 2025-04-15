from pydantic import BaseModel
from .perception import LLMResponse

class ActionInput(BaseModel):
    llm_response: LLMResponse


def perform_action(action_input: ActionInput):
    # For now, just print the LLM's response
    print(f"Agent Response: {action_input.llm_response.response}")
