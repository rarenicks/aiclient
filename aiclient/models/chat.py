from typing import Iterator, Dict, Any, Union, List, Type, TypeVar
import json
from pydantic import BaseModel
from ..types import ModelResponse, BaseMessage, SystemMessage, UserMessage
from ..transport.base import Transport
from ..providers.base import Provider

T = TypeVar("T", bound=BaseModel)

class ChatModel:
    """Wrapper for chat model interactions using a Provider strategy."""
    def __init__(self, model_name: str, provider: Provider, transport: Transport):
        self.model_name = model_name
        self.provider = provider
        self.transport = transport

    def generate(self, prompt: Union[str, List[BaseMessage]], response_model: Type[T] = None) -> Union[ModelResponse, T]:
        """
        Generate a response synchronously.
        If response_model is provided, returns an instance of that model.
        Otherwise returns ModelResponse.
        """
        messages = prompt
        if isinstance(prompt, str):
            messages = [UserMessage(content=prompt)]
        
        # Handling Structured Output
        if response_model:
            schema = response_model.model_json_schema()
            instruction = (
                f"\n\nRestricted Output Mode: You must response strictly with a valid JSON object that matches the following JSON Schema.\n"
                f"Do not return the schema itself. Return the data instance.\n"
                f"Schema:\n{json.dumps(schema, indent=2)}"
            )
            
            # Inject into system prompt if available, else append to last user message
            # Simple strategy: append to last message content
            if messages and isinstance(messages[-1], UserMessage):
                new_content = messages[-1].content + instruction
                messages[-1] = UserMessage(content=new_content)
            else:
                 messages.append(UserMessage(content=instruction))

        endpoint, data = self.provider.prepare_request(self.model_name, messages)
        response_data = self.transport.send(endpoint, data)
        model_response = self.provider.parse_response(response_data)
        
        if response_model:
            try:
                # Basic cleanup for code blocks (```json ... ```)
                text = model_response.text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    if text.endswith("```"):
                        text = text.rsplit("\n", 1)[0]
                
                parsed = json.loads(text)
                return response_model.model_validate(parsed)
            except (json.JSONDecodeError, ValueError) as e:
                # In v0.2, just raise or returning raw failed response might be better. 
                # For now, let's error to be explicit.
                raise ValueError(f"Failed to parse structured output: {e}. Raw: {model_response.text}")

        return model_response

    def stream(self, prompt: Union[str, List[BaseMessage]]) -> Iterator[str]:
        """Stream a response synchronously."""
        endpoint, data = self.provider.prepare_request(self.model_name, prompt)
        for chunk_data in self.transport.stream(endpoint, data):
            chunk = self.provider.parse_stream_chunk(chunk_data)
            if chunk:
                yield chunk.text

class SimpleResponse:
    def __init__(self, text: str, raw: Dict[str, Any]):
        self.text = text
        self.raw = raw
