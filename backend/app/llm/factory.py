import os
from app.llm.provider import DummyVisionProvider, DummyChatProvider, VisionProviderBase, ChatProviderBase

# Provider-Auswahl über ENV oder Config
VISION_PROVIDER = os.environ.get("VISION_PROVIDER", "dummy")
CHAT_PROVIDER = os.environ.get("CHAT_PROVIDER", "dummy")

def get_vision_provider() -> VisionProviderBase:
    if VISION_PROVIDER == "dummy":
        return DummyVisionProvider()
    # Hier können weitere Provider ergänzt werden
    raise ValueError(f"Unbekannter Vision Provider: {VISION_PROVIDER}")

def get_chat_provider() -> ChatProviderBase:
    if CHAT_PROVIDER == "dummy":
        return DummyChatProvider()
    # Hier können weitere Provider ergänzt werden
    raise ValueError(f"Unbekannter Chat Provider: {CHAT_PROVIDER}")
