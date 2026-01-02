import contextlib
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    A wrapper around the Model Context Protocol (MCP) client.
    Manages connections to MCP servers and provides tool discovery.
    """

    def __init__(
        self, command: str, args: List[str], env: Optional[Dict[str, str]] = None
    ):
        self.params = StdioServerParameters(command=command, args=args, env=env)
        self.session: Optional[ClientSession] = None
        self._exit_stack = contextlib.AsyncExitStack()

    async def __aenter__(self):
        # Establish connection
        read, write = await self._exit_stack.enter_async_context(
            stdio_client(self.params)
        )
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await self.session.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.aclose()
        self.session = None

    async def list_tools(self) -> List[Any]:
        if not self.session:
            raise RuntimeError("MCP Client not connected. Use 'async with client:'.")
        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not self.session:
            raise RuntimeError("MCP Client not connected")
        return await self.session.call_tool(name, arguments=arguments)
