from pydantic import BaseModel
from .perception import LLMResponse
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from rich.panel import Panel

console = Console()
mcp = FastMCP("ActionMCP")

class ActionInput(BaseModel):
    llm_response: LLMResponse


def perform_action(action_input: ActionInput):
    # For now, just print the LLM's response
    print(f"Agent Response: {action_input.llm_response.response}")
