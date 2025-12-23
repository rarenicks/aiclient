from pydantic import BaseModel
from aiclient import Client

class Character(BaseModel):
    name: str
    class_type: str
    level: int
    items: list[str]

client = Client()

def main():
    print("--- Structured Outputs Example ---")
    
    # 1. Native Restricted Mode (OpenAI)
    # Requires 'strict=True'
    try:
        print("\n1. OpenAI Native Strict Mode:")
        char = client.chat("gpt-4o").generate(
            "Generate a level 5 wizard named Merlin with a staff and hat.",
            response_model=Character,
            strict=True
        )
        print(f"Valid Character: {char}")
    except Exception as e:
        print(f"Skipping OpenAI demo (missing key?): {e}")

    # 2. Universal Fallback (Anthropic/Others)
    # strict=False (default) uses prompt injection
    try:
        print("\n2. Universal Fallback (Claude):")
        char = client.chat("claude-3-opus-20240229").generate(
            "Generate a level 10 warrior named Conan.",
            response_model=Character
        )
        print(f"Valid Character: {char}")
    except Exception as e:
        print(f"Skipping Claude demo: {e}")

if __name__ == "__main__":
    main()
