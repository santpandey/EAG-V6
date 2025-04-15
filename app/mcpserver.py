from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from rich.panel import Panel
from brain.memory import MemoryStore, MemoryItem
from brain.perception import call_external_llm
from brain.decision_making import craft_prompt
from brain.action import perform_action
from brain.decision_making import DecisionInput
from brain.action import ActionInput

console = Console()
mcp = FastMCP("MCPServer")

@mcp.tool("/memory")
def handle_memory(message: TextContent):
    memory_store = MemoryStore()
    memory_store.add_item(MemoryItem(type="preference", content=message.text.strip()))
    return TextContent(text="Memory updated")


@mcp.tool("perception")
def handle_perception(request: LLMRequest):
    return call_external_llm(request)

@mcp.tool("DecisionMaking")
def handle_decision_making(input_data: DecisionInput):
    return craft_prompt(input_data)

@mcp.tool("action")
def handle_action(action_input: ActionInput):
    return perform_action(action_input)
