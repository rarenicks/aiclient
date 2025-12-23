import asyncio
import os
from aiclient import Client
from aiclient.agent import Agent

def get_weather(location: str):
    """Get the current weather for a location."""
    if "sf" in location.lower() or "san francisco" in location.lower():
        return "Sunny, 25C"
    elif "london" in location.lower():
        return "Rainy, 10C"
    return "Unknown"

async def main():
    print("🤖 AGENT VERIFICATION")
    print("======================")
    
    client = Client()
    # Use OpenAI for robust tool following
    model = client.chat("gpt-4o")
    
    agent = Agent(model, tools=[get_weather])
    
    prompt = "What is the weather in San Francisco? And in London?"
    print(f"Prompt: {prompt}")
    
    try:
        # Test Async Run
        response = await agent.run_async(prompt)
        print(f"\nFinal Response:\n{response}")
        
        if "sunny" in response.lower() and "rainy" in response.lower():
             print("✅ Agent loop working (Multiple tools executed)")
        else:
             print("⚠️ Unexpected response content")
             
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(e, "response"):
            print(f"Body: {e.response.text}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
