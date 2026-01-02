from unittest.mock import AsyncMock, patch

import pytest

from aiclient.mcp.client import MCPClient
from aiclient.mcp.manager import MCPServerManager


@pytest.mark.asyncio
async def test_mcp_client_connection():
    # Mock stdio_client and ClientSession
    with (
        patch("aiclient.mcp.client.stdio_client") as mock_stdio,
        patch("aiclient.mcp.client.ClientSession") as mock_session_cls,
    ):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session_cls.return_value = mock_session

        # Async context manager mock for stdio_client
        mock_stdio_ctx = AsyncMock()
        mock_stdio.return_value = mock_stdio_ctx
        mock_stdio_ctx.__aenter__.return_value = (
            AsyncMock(),
            AsyncMock(),
        )  # read, write

        client = MCPClient("ls", ["-la"])
        async with client:
            assert client.session is not None
            # Verify initialization called
            mock_session.initialize.assert_awaited()

        assert client.session is None


@pytest.mark.asyncio
async def test_server_manager():
    manager = MCPServerManager()
    manager.add_server("test", "echo", ["hello"])

    assert "test" in manager._clients
    client = await manager.get_client("test")
    assert isinstance(client, MCPClient)
    assert client.params.command == "echo"
