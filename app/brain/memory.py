from pydantic import BaseModel
from typing import List, Any
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from rich.panel import Panel

console = Console()
mcp = FastMCP("MemoryMCP")

class MemoryItem(BaseModel):
    user: str  # e.g., 'preference', 'fact', 'answer'
    content: Any

class MemoryStore(BaseModel):
    items: List[MemoryItem] = []

    def add_item(self, item: MemoryItem):
        self.items.append(item)
    def get_items_by_user(self, user_filter: str) -> List[MemoryItem]:
        return [item for item in self.items if item.user == user_filter]
    def get_all(self) -> List[MemoryItem]:
        return self.items
