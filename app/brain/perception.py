from pydantic import BaseModel
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from rich.panel import Panel

console = Console()
mcp = FastMCP("PerceptionMCP")

class LLMRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 256
    additional_params: Dict[str, Any] = {}

class LLMResponse(BaseModel):
    response: str
    usage: Dict[str, Any] = {}

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def call_external_llm(request: LLMRequest) -> LLMResponse:
    # TODO: Integrate with real LLM API (e.g., Google Gemini)
    # For now, return a dummy response
    response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=request.prompt,
        )
    print("response is ",response.text.strip())
    usage = {"model": request.model, "tokens": request.max_tokens}
    return LLMResponse(response=response.text.strip(), usage=usage)
