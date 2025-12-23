"""
Tests for Tool functionality and schema generation.
"""
import pytest
from pydantic import BaseModel, Field
from aiclient.tools.base import Tool


def simple_function(text: str) -> str:
    """A simple function that echoes text."""
    return f"Echo: {text}"


def function_with_defaults(name: str, age: int = 25, city: str = "NYC") -> str:
    """Function with default parameters."""
    return f"{name}, {age}, {city}"


def function_no_docstring(x: int) -> int:
    return x * 2


def test_tool_from_function():
    """Test Tool.from_fn wraps a function correctly."""
    tool = Tool.from_fn(simple_function)

    assert tool.name == "simple_function"
    assert tool.description == "A simple function that echoes text."
    assert tool.fn == simple_function


def test_tool_schema_generation():
    """Test tool generates correct JSON schema for arguments."""
    def weather_tool(location: str, units: str = "celsius") -> str:
        """Get weather for a location."""
        return f"Weather in {location}"

    tool = Tool.from_fn(weather_tool)

    schema = tool.args_schema.model_json_schema()

    assert "location" in schema["properties"]
    assert "units" in schema["properties"]
    assert "location" in schema["required"]
    assert "units" not in schema["required"]  # Has default


def test_tool_execution():
    """Test tool can execute wrapped function."""
    def add_numbers(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    tool = Tool.from_fn(add_numbers)

    result = tool.fn(a=5, b=3)
    assert result == 8


def test_tool_with_complex_types():
    """Test tool handles complex parameter types."""

    def process_data(
        items: list[str],
        metadata: dict[str, int],
        enabled: bool = True
    ) -> str:
        """Process data with complex types."""
        return f"Processed {len(items)} items"

    tool = Tool.from_fn(process_data)

    schema = tool.args_schema.model_json_schema()

    assert schema["properties"]["items"]["type"] == "array"
    assert schema["properties"]["metadata"]["type"] == "object"
    assert schema["properties"]["enabled"]["type"] == "boolean"


def test_tool_no_docstring_uses_function_name():
    """Test tool handles functions without docstrings."""
    tool = Tool.from_fn(function_no_docstring)

    assert tool.name == "function_no_docstring"
    # Description might be empty or function name
    assert tool.description is not None


def test_tool_with_pydantic_field():
    """Test tool can use Pydantic Field for descriptions."""

    def search(query: str = Field(description="The search query")) -> str:
        """Search for information."""
        return f"Results for: {query}"

    tool = Tool.from_fn(search)
    schema = tool.args_schema.model_json_schema()

    # Pydantic Field description should be in schema
    assert "query" in schema["properties"]


def test_tool_manual_creation():
    """Test creating Tool manually."""

    class SearchArgs(BaseModel):
        query: str
        limit: int = 10

    def search_fn(query: str, limit: int = 10) -> str:
        return f"Found {limit} results for {query}"

    tool = Tool(
        name="custom_search",
        description="Custom search tool",
        fn=search_fn,
        schema=SearchArgs  # Note: parameter is 'schema' not 'args_schema'
    )

    assert tool.name == "custom_search"
    assert tool.description == "Custom search tool"
    assert tool.fn == search_fn


def test_tool_with_no_parameters():
    """Test tool with function that takes no parameters."""

    def get_current_time() -> str:
        """Get the current time."""
        return "12:00 PM"

    tool = Tool.from_fn(get_current_time)

    schema = tool.args_schema.model_json_schema()
    assert schema["properties"] == {}  # No parameters


def test_tool_preserves_function_signature():
    """Test tool preserves original function for execution."""

    def multiply(x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y

    tool = Tool.from_fn(multiply)

    result = tool.fn(x=2.5, y=4.0)
    assert result == 10.0


def test_tool_multiple_tools_from_functions():
    """Test creating multiple tools from different functions."""

    def tool1(a: str) -> str:
        """First tool."""
        return a

    def tool2(b: int) -> int:
        """Second tool."""
        return b

    tools = [Tool.from_fn(tool1), Tool.from_fn(tool2)]

    assert len(tools) == 2
    assert tools[0].name == "tool1"
    assert tools[1].name == "tool2"
    assert tools[0].fn != tools[1].fn
