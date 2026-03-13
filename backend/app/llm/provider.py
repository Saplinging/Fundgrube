import time
from typing import Any

class VisionProviderBase:
    def describe(self, image_path: str | bytes) -> dict:
        """
        Nimmt einen Bildpfad oder Bildbytes und gibt eine Beschreibung zurück.
        Muss von konkreten Providern implementiert werden.
        """
        raise NotImplementedError

class DummyVisionProvider(VisionProviderBase):
    def describe(self, image_path: str | bytes) -> dict:
        start = time.time()
        # Dummy-Implementierung
        desc = "Dies ist ein Dummy-Bildbeschreibungstext."
        latency = int((time.time() - start) * 1000)
        return {"description": desc, "model": "dummy", "latency_ms": latency}

class ChatProviderBase:
    def chat(self, prompt: str, context: Any = None) -> dict:
        """
        Nimmt Prompt und optional Kontext, gibt Antworttext zurück.
        Muss von konkreten Providern implementiert werden.
        """
        raise NotImplementedError

class DummyChatProvider(ChatProviderBase):
    def chat(self, prompt: str, context: Any = None) -> dict:
        start = time.time()
        answer = f"Dummy-Antwort auf: {prompt}"
        latency = int((time.time() - start) * 1000)
        return {"answer": answer, "model": "dummy", "latency_ms": latency}
