# Backend

## Lokales Starten

1. Python 3.9+ installieren
2. Abhängigkeiten installieren:
	```
	pip install fastapi uvicorn
	```
3. Backend starten:
	```
	uvicorn app.main:app --reload
	```

Das Backend läuft dann unter http://127.0.0.1:8000

## Provider-System (Modularität)

- Vision-, Chat- und Embedding-Provider sind modular aufgebaut und über ENV-Variablen auswählbar:
	- `VISION_PROVIDER` (dummy/ollama/api)
	- `CHAT_PROVIDER` (dummy/ollama/api)
	- `EMBEDDING_PROVIDER` (dummy, weitere möglich)
- Die Factory-Pattern-Implementierung findet sich in `app/llm/factory.py` (Vision/Chat) und `app/rag/factory.py` (Embedding).
- Standardmäßig ist überall ein Dummy-Provider aktiv.

## Endpunkte

- **GET /health**: Health Check, gibt `{ "status": "ok" }` zurück.