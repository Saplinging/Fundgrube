import requests
from .provider import VisionProviderBase, ChatProviderBase

class OllamaVisionProvider(VisionProviderBase):
    def describe(self, image_path: str | bytes) -> dict:
        # Beispiel: Lokale Ollama-API für Bildbeschreibung
        # Hier Dummy-Implementierung, da Ollama Vision ggf. nicht verfügbar
        return {"description": "Ollama Vision nicht implementiert", "model": "ollama"}

class OllamaChatProvider(ChatProviderBase):
    def chat(self, prompt: str, context: any = None) -> dict:
        # Beispiel: Lokale Ollama-API für Chat
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama2", "prompt": prompt, "stream": False},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return {"answer": data.get("response", ""), "model": "ollama"}
        except Exception as e:
            return {"answer": f"Ollama Fehler: {e}", "model": "ollama"}
