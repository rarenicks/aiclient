# aiclient-llm

[![PyPI version](https://badge.fury.io/py/aiclient-llm.svg)](https://badge.fury.io/py/aiclient-llm)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**A minimal, unified, and resilient Python client for modern LLMs.**

Supports **OpenAI**, **Anthropic** (Claude 3), **Google** (Gemini), and **xAI** (Grok) with a single, consistent interface.



## Documentation

- [**Getting Started**](docs/getting_started.md): Installation, Configuration, Basic Usage.
- [**Features Guide**](docs/features.md): Agents, Multimodal, Local LLMs (Ollama), Structured Output.
- [**Middleware**](docs/middleware.md): Cost tracking, logging, and custom middleware.

## Key Features

- 🦄 **Unified Interface**: Swap between OpenAI, Anthropic, Google, xAI, and Ollama seamlessly.
- ⚡ **Async & Sync**: Native asyncio support for high-performance apps.
- 🚀 **Prompt Caching**: Native support for Anthropic Prompt Caching headers (v0.4).
- 🏗️ **Structured Outputs**: Native strict JSON Schema support for OpenAI (v0.4).
- 🛡️ **Resilient**: Circuit Breakers, Rate Limiters, and automatic retries (v0.4).
- 🔭 **Observability**: Tracing and OpenTelemetry hooks (v0.4).
- 🤖 **Agent Primitives**: Built-in ReAct loop for tool-using agents.
- 📊 **Middleware**: Inspect requests, track costs, or log data.

## Installation

```bash
pip install aiclient-llm
```

*(Note: Not yet on PyPI, install from source/git)*

## Quick Start

### Basic Chat

```python
from aiclient import Client

client = Client(
    api_key_openai="sk-...", 
    api_key_anthropic="sk-ant-..."
)

# Call OpenAI
response = client.chat("gpt-4o").generate("Hello!")
print(response.text)

# Call Claude
response = client.chat("claude-3-opus-20240229").generate("Hello!")
print(response.text)
```

### Multimodal (Vision)

```python
from aiclient.types import UserMessage, Text, Image

msg = UserMessage(content=[
    Text(text="What's in this image?"),
    Image(path="./image.png") # Handles base64 automatically
])

response = client.chat("gpt-4o").generate([msg])
print(response.text)
```

### Agents (Tool Use)

```python
from aiclient.agent import Agent

def get_weather(location: str):
    return "Sunny in " + location

agent = Agent(
    model=client.chat("gpt-4o"),
    tools=[get_weather]
)

print(agent.run("Weather in SF?"))
```

### Local LLMs (Ollama) 🏠

Use the `provider:model` syntax to route requests to local models (e.g., via Ollama).

```python
# Connects to http://localhost:11434/v1 by default
client.chat("ollama:llama3").generate("Why is the sky blue?")

# Connect to custom URL (e.g. LMStudio)
client = Client(ollama_base_url="http://localhost:1234/v1")
client.chat("ollama:mistral").generate("Hi")
```

### Streaming

```python
for chunk in client.chat("gpt-4o").stream("Write a poem"):
    print(chunk.text, end="", flush=True)
```

## Configuration

### Retries

```python
# Retries up to 3 times with backoff
client = Client(max_retries=3, retry_delay=1.0)
```

## License

Apache-2.0
