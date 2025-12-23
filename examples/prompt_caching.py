import os
from aiclient import Client, SystemMessage, UserMessage

# Ensure you have ANTHROPIC_API_KEY env var set
client = Client()

def main():
    print("--- Prompt Caching Example (Anthropic) ---")
    
    # 1. Define a long system prompt (cached)
    system_text = "You are a helpful assistant. " * 500 # Simulate length
    
    messages = [
        SystemMessage(content=system_text, cache_control="ephemeral"),
        UserMessage(content="Hello, how are you?", cache_control="ephemeral")
    ]
    
    # 2. First call (Cache Creation)
    print("\nSending Request 1 (Cache Creation)...")
    resp1 = client.chat("claude-3-5-sonnet-20240620").generate(messages)
    print(f"Response: {resp1.text}")
    print(f"Creation Tokens: {resp1.usage.cache_creation_input_tokens}")
    print(f"Read Tokens:     {resp1.usage.cache_read_input_tokens}")

    # 3. Second call with same prefix (Cache Hit)
    print("\nSending Request 2 (Cache Hit)...")
    # Note: In real usage, usually <5min TTL. 
    resp2 = client.chat("claude-3-5-sonnet-20240620").generate(messages)
    print(f"Response: {resp2.text}")
    print(f"Creation Tokens: {resp2.usage.cache_creation_input_tokens}")
    print(f"Read Tokens:     {resp2.usage.cache_read_input_tokens}")

if __name__ == "__main__":
    main()
