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

## Endpunkte

- **GET /health**: Health Check, gibt `{ "status": "ok" }` zurück.