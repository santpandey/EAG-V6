from pydantic import BaseModel
from typing import Any, Dict, Optional
import os
from dotenv import load_dotenv
from google import genai
from typing import Optional

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class LLMRequest(BaseModel):
    prompt: str
    image_b64: Optional[str] = None
    additional_params: Dict[str, Any] = {}

class LLMResponse(BaseModel):
    response: str
    usage: Dict[str, Any] = {}



def call_external_llm(request: LLMRequest) -> LLMResponse:
    try:
        parts = []
        if request.prompt:
            parts.append({"text": request.prompt})
        if request.image_b64:
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",  # Default, can be adjusted
                    "data": request.image_b64
                }
            })
        contents = [{"role": "user", "parts": parts}]
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
        # Try to extract text and usage from Gemini response
        text = getattr(response, 'text', None)
        if text is None and hasattr(response, 'result'):  # fallback if structure differs
            text = getattr(response.result, 'text', None)
        usage = {}
        if hasattr(response, 'usage'):
            usage = dict(response.usage)
        print(f'Text: {text}\n\nUsage: {usage}')
        return LLMResponse(response=text.strip() if text else '', usage=usage)
    except Exception as e:
        # Always return a valid Pydantic object, even on error
        return LLMResponse(response=f"Error: {str(e)}", usage={})
