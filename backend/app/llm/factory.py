import os
import logging
from app.llm.provider import DummyVisionProvider, DummyChatProvider, VisionProviderBase, ChatProviderBase
from app.llm.ollama_provider import OllamaVisionProvider, OllamaChatProvider
from app.llm.api_provider import ApiVisionProvider, ApiChatProvider

# Provider-Auswahl über ENV oder Config
VISION_PROVIDER = os.environ.get("VISION_PROVIDER", "dummy").lower()
CHAT_PROVIDER = os.environ.get("CHAT_PROVIDER", "dummy").lower()

def get_vision_provider() -> VisionProviderBase:
    if VISION_PROVIDER == "dummy":
        logging.info("VisionProvider: DummyVisionProvider aktiv")
        return DummyVisionProvider()
    if VISION_PROVIDER == "ollama":
        logging.info("VisionProvider: OllamaVisionProvider aktiv")
        return OllamaVisionProvider()
    if VISION_PROVIDER == "api" or VISION_PROVIDER == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logging.warning("OPENAI_API_KEY nicht gesetzt, API VisionProvider kann nicht genutzt werden!")
        logging.info("VisionProvider: ApiVisionProvider aktiv")
        return ApiVisionProvider()
    raise ValueError(f"Unbekannter Vision Provider: {VISION_PROVIDER}")

def get_chat_provider() -> ChatProviderBase:
    if CHAT_PROVIDER == "dummy":
        logging.info("ChatProvider: DummyChatProvider aktiv")
        return DummyChatProvider()
    if CHAT_PROVIDER == "ollama":
        logging.info("ChatProvider: OllamaChatProvider aktiv")
        return OllamaChatProvider()
    if CHAT_PROVIDER == "api" or CHAT_PROVIDER == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logging.warning("OPENAI_API_KEY nicht gesetzt, API ChatProvider kann nicht genutzt werden!")
        logging.info("ChatProvider: ApiChatProvider aktiv")
        return ApiChatProvider()
    raise ValueError(f"Unbekannter Chat Provider: {CHAT_PROVIDER}")
