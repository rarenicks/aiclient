from pydantic import BaseModel

from .base import Tool


class PolicyCheckSchema(BaseModel):
    text: str


def check_policy(text: str) -> bool:
    """Check if text complies with policy."""
    return "forbidden" not in text


policy_tool = Tool(
    name="check_policy",
    fn=check_policy,
    schema=PolicyCheckSchema,
    description="Checks if the text complies with content policy.",
)
