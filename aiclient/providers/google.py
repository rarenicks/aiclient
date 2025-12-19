import json
from typing import Any, Dict, Tuple, Optional, Union, List
from .base import Provider
from ..types import ModelResponse, StreamChunk, Usage, BaseMessage, UserMessage

class GoogleProvider(Provider):
    def __init__(self, api_key: str, base_url: str = "https://generativelanguage.googleapis.com/v1beta"):
        self.api_key = api_key
        self._base_url = base_url.rstrip("/")

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
        }

    def prepare_request(self, model: str, prompt: Union[str, List[BaseMessage]]) -> Tuple[str, Dict[str, Any]]:
        contents = []
        if isinstance(prompt, str):
            contents.append({"role": "user", "parts": [{"text": prompt}]})
        else:
            for msg in prompt:
                role = "model" if msg.role == "assistant" else "user"
                # Gemini doesn't support 'system' role in `generateContent` messages list easily (uses system_instruction)
                # For simplicity in v1, we treat system as user or ignore. Let's merge it into user for now or revisit.
                # Actually, Gemini 1.5 supports system instructions, but let's stick to simple role mapping for now.
                if msg.role == "system":
                    # Primitive handling: Prepend system prompt to next user message or just add as user
                    contents.append({"role": "user", "parts": [{"text": f"System: {msg.content}"}]})
                else:
                    contents.append({"role": role, "parts": [{"text": msg.content}]})

        endpoint = f"/models/{model}:generateContent?key={self.api_key}"
        payload = {"contents": contents}
        return endpoint, payload

    def parse_response(self, response_data: Dict[str, Any]) -> ModelResponse:
        try:
             content = response_data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
             content = ""
             
        meta = response_data.get("usageMetadata", {})
        usage = Usage(
            input_tokens=meta.get("promptTokenCount", 0),
            output_tokens=meta.get("candidatesTokenCount", 0),
            total_tokens=meta.get("totalTokenCount", 0),
        )

        return ModelResponse(
            text=content, 
            raw=response_data,
            usage=usage,
            provider="google"
        )

    def parse_stream_chunk(self, chunk: Dict[str, Any]) -> Optional[StreamChunk]:
        # Google streaming format is a bit different (array of JSON objects)
        # Placeholder for complex stream parsing which might differ from basic SSE
        return None 
