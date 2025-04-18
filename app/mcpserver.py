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

# Persistent memory store for all users
memory_store = MemoryStore()

def get_system_prompt():
    with open("app/system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def orchestrate(message: str, username: str, download_summary: bool = False, email: str = None):
    """
    Orchestrates the routing of the message to the appropriate brain module.
    Uses a persistent MemoryStore for all users.
    """
    user_memories = memory_store.get_items_by_user(username)
    if user_memories:
        # User exists, append the new message
        memory_store.add_item(MemoryItem(user=username, content=message))
    else:
        # New user, create first entry
        memory_store.add_item(MemoryItem(user=username, content=message))
    # Pass only this user's memory to DecisionInput
    user_memory_store = MemoryStore(items=memory_store.get_items_by_user(username))
    # Read system prompt from file
    system_prompt = get_system_prompt()
    decision_input = DecisionInput(user_input=message, memory=user_memory_store)
    decision_output = craft_prompt(decision_input, system_prompt=system_prompt)
    response = {"crafted_prompt": decision_output.crafted_prompt}
    if download_summary:
        response["download_summary"] = True
    if email:
        response["email_sent_to"] = email
    return response

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
