from pydantic import BaseModel
from typing import List
from .memory import MemoryStore, MemoryItem
from .perception import LLMRequest
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from rich.panel import Panel

console = Console()
mcp = FastMCP("DecisionMakingMCP")

class DecisionInput(BaseModel):
    user_input: str
    memory: MemoryStore

class DecisionOutput(BaseModel):
    crafted_prompt: str


def craft_prompt(input_data: DecisionInput) -> DecisionOutput:
    # Gather relevant facts/preferences/answers from memory
    memory_snippets = [item.content for item in input_data.memory.get_all()]
    context = '\n'.join([str(snippet) for snippet in memory_snippets])
    crafted_prompt = f"Context:\n{context}\n\nUser: {input_data.user_input}\nAgent:"
    return DecisionOutput(crafted_prompt=crafted_prompt)
