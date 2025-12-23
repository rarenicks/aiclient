# Features

## Local LLMs (Ollama & LMStudio) 🏠

`aiclient-llm` supports routing requests to local inference servers using the `provider:model` syntax.

### Usage
Default (Ollama):
```python
# Connects to http://localhost:11434/v1
response = client.chat("ollama:llama3").generate("Hi")
```

Custom URL (e.g., LMStudio, remote server):
```python
client = Client(ollama_base_url="http://192.168.1.5:1234/v1")
response = client.chat("ollama:mistral").generate("Hi")
```

## Agents & Tool Use 🤖

Build powerful agents using the `Agent` class, which implements a ReAct loop.

```python
from aiclient import Client, Agent

def get_weather(city: str):
    return f"Sunny in {city}"

client = Client()
agent = Agent(
    model=client.chat("gpt-4o"),
    tools=[get_weather],
    max_steps=10
)

result = agent.run("What's the weather in Tokyo?")
print(result)
```

## Multimodal (Vision) 👁️

Send images easily to models that support it (GPT-4o, Claude 3, Gemini, etc.).

```python
from aiclient.types import UserMessage, Text, Image

msg = UserMessage(content=[
    Text(text="Analyze this diagram"),
    Image(path="./chart.png") # Automatically base64 encoded
])

response = client.chat("gpt-4o").generate([msg])
```

## Prompt Caching (Cost Optimization) 💰

Reduce costs by up to 90% and latency by up to 85% with prompt caching. Currently supported on Anthropic (Claude 3.5 Sonnet/Haiku/Opus).

### Usage

Mark cache breakpoints using the `cache_control` parameter on messages.

```python
from aiclient import Client, SystemMessage, UserMessage

client = Client(api_key_anthropic="...")

messages = [
    # Cache system prompt (e.g. large context docs)
    SystemMessage(
        content="<long text field>...", 
        cache_control="ephemeral"
    ),
    # Cache up to the last turn of conversation
    UserMessage(content="Hello", cache_control="ephemeral")
]

response = client.chat("claude-3-5-sonnet-20240620").generate(messages)

# Check savings
print(f"Cache Creation Tokens: {response.usage.cache_creation_input_tokens}")
print(f"Cache Read Tokens: {response.usage.cache_read_input_tokens}")
```

## Structured Output (Pydantic) 📦

Validate responses against a schema. V0.4 adds support for **Native Structured Outputs** (e.g., OpenAI `response_format`), guaranteeing 100% schema adherence.

```python
from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    age: int

# 1. Native Restricted Mode (strict=True) - OpenAI only for now
user = client.chat("gpt-4o").generate(
    "John is 25 years old", 
    response_model=UserInfo,
    strict=True
)

# 2. Universal Fallback (strict=False) - Works on all providers via prompt injection
user = client.chat("claude-3-opus").generate(
    "John is 25 years old", 
    response_model=UserInfo
)

print(user.name, user.age)
```
