import requests
import os
from .provider import VisionProviderBase, ChatProviderBase

class ApiVisionProvider(VisionProviderBase):
    def describe(self, image_path: str | bytes) -> dict:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"description": "Kein API-Key gesetzt", "model": "api"}
        # Beispiel: OpenAI Vision API (Pseudo-Code)
        return {"description": "API Vision nicht implementiert", "model": "api"}

class ApiChatProvider(ChatProviderBase):
    def chat(self, prompt: str, context: any = None) -> dict:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"answer": "Kein API-Key gesetzt", "model": "api"}
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return {"answer": data["choices"][0]["message"]["content"], "model": "api"}
        except Exception as e:
            return {"answer": f"API Fehler: {e}", "model": "api"}
