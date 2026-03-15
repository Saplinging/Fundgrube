import requests
import os
from .provider import VisionProviderBase, ChatProviderBase

class ApiVisionProvider(VisionProviderBase):
    def describe(self, image_path: str | bytes) -> dict:
        import base64
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"description": "Kein API-Key gesetzt", "model": "api"}
        try:
            # Bilddaten laden
            if isinstance(image_path, bytes):
                image_bytes = image_path
            else:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Beschreibe das Bild."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }
                ],
                "max_tokens": 512
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            description = data["choices"][0]["message"]["content"]
            return {"description": description, "model": "openai-vision"}
        except Exception as e:
            return {"description": f"OpenAI Vision Fehler: {e}", "model": "openai-vision"}

class ApiChatProvider(ChatProviderBase):
    def chat(self, messages_or_prompt, context: any = None) -> dict:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"answer": "Kein API-Key gesetzt", "model": "api"}
        try:
            if isinstance(messages_or_prompt, list):
                messages = messages_or_prompt
            else:
                messages = [{"role": "user", "content": messages_or_prompt}]
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-4o",
                    "messages": messages
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return {"answer": data["choices"][0]["message"]["content"], "model": "api"}
        except Exception as e:
            return {"answer": f"API Fehler: {e}", "model": "api"}
