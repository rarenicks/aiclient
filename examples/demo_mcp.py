import asyncio

from aiclient import Agent, Client

# Requires 'npx' available in path if using Node.js servers
# Or local python servers


async def main():
    print("--- MCP Agent Demo (Filesystem) ---")

    # Configuration for the official filesystem MCP server
    # Requires: npm install -g @modelcontextprotocol/server-filesystem (or npx usage)
    mcp_servers = {
        "fs": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"],
        }
    }

    client = Client()

    # Note: Agent usage as context manager is recommended for MCP
    print("Initializing agent...")
    agent = Agent(
        model=client.chat("gpt-4o"),  # Mocks or real key required
        mcp_servers=mcp_servers,
    )

    async with agent:
        print("Connected to MCP servers.")

        # In a real run with OpenAI key, this would list files
        # For demo purposes, we just print tools if we could inspect them
        # (Internal API for debugging)
        # tools = await agent.mcp_manager.list_global_tools()
        # print(f"Available tools: {[t.name for t in tools]}")

        # response = await agent.run_async("List the files in this directory")
        # print("Response:", response)
        print("Demo structure ready. Uncomment lines to run with real API key and npx.")


if __name__ == "__main__":
    asyncio.run(main())
