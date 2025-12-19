from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel

class BaseMessage(BaseModel):
    role: str
    content: str

class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"

class UserMessage(BaseMessage):
    role: Literal["user"] = "user"

class AssistantMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"

class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

class ModelResponse(BaseModel):
    """Standardized response from any AI provider."""
    text: str
    raw: Dict[str, Any]
    usage: Usage = Usage()
    provider: str = "unknown"

class StreamChunk(BaseModel):
    """Standardized stream chunk."""
    text: str
    delta: str
