from pydantic import BaseModel
from .perception import LLMResponse
from typing import Dict, Any


class ActionInput(BaseModel):
    llm_response: LLMResponse

class ResponseModel(BaseModel):
    crafted_prompt: str
    download_summary: str = None
    summary_file: str = None
    email_sent_to: str = None
    image_filename: str = None

class FinalResponse(BaseModel):
    response: str
    usage: Dict[str, Any] = {}


def perform_action(action_input: ActionInput):
    # For now, just print the LLM's response
    print(f"Agent Response: {action_input.llm_response.response}")
