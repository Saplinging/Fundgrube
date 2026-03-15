import requests
from .provider import VisionProviderBase, ChatProviderBase

class OllamaVisionProvider(VisionProviderBase):
    def describe(self, image_path: str | bytes) -> dict:
        import base64
        import os
        try:
            # Bilddaten laden
            if isinstance(image_path, bytes):
                image_bytes = image_path
            else:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            # base64-kodieren
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            # Base URL aus ENV
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            generate_url = f"{base_url.rstrip('/')}/api/generate"
            model_name = os.environ.get("OLLAMA_VISION_MODEL", "llava:latest")
            payload = {
                "model": model_name,
                "images": [image_b64],
                "prompt": "Beschreibe das Bild.",
                "stream": False
            }
            response = requests.post(
                generate_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            # Die Antwortstruktur kann je nach Ollama-Version variieren
            description = data.get("response") or data.get("description") or str(data)
            return {"description": description, "model": "ollama"}
        except Exception as e:
            return {"description": f"Ollama Vision Fehler: {e}", "model": "ollama"}

class OllamaChatProvider(ChatProviderBase):
    def chat(self, prompt: str, context: any = None) -> dict:
        # Beispiel: Lokale Ollama-API für Chat
        import os
        try:
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            chat_url = f"{base_url.rstrip('/')}/api/generate"
            model_name = os.environ.get("OLLAMA_CHAT_MODEL", "llama2")
            response = requests.post(
                chat_url,
                json={"model": model_name, "prompt": prompt, "stream": False},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return {"answer": data.get("response", ""), "model": "ollama"}
        except Exception as e:
            return {"answer": f"Ollama Fehler: {e}", "model": "ollama"}
