from pydantic import BaseModel
from .memory import MemoryStore
from .perception import LLMRequest


class DecisionInput(BaseModel):
    user_input: str
    memory: MemoryStore

class DecisionOutput(BaseModel):
    crafted_prompt: str


def craft_prompt(input_data: DecisionInput, system_prompt: str = None) -> DecisionOutput:
    # Gather relevant facts/preferences/answers from memory
    memory_snippets = [item.content for item in input_data.memory.get_all()]
    context = '\n'.join([str(snippet) for snippet in memory_snippets])
    crafted_prompt = ""
    if system_prompt:
        crafted_prompt += f"System Prompt:\n{system_prompt}\n\n"
    crafted_prompt += f"Context:\n{context}\n\nUser: {input_data.user_input}\n"
    return DecisionOutput(crafted_prompt=crafted_prompt)

