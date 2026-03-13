# Architektur

## LLM Provider Schnittstelle

### Verfügbare Provider
- DummyVisionProvider (Standard)
- DummyChatProvider (Standard)

### Provider-Auswahl
Die Auswahl des Vision- und Chat-Providers erfolgt ausschließlich über ENV-Variablen:

- `VISION_PROVIDER` (z.B. "dummy")
- `CHAT_PROVIDER` (z.B. "dummy")

Weitere Provider können durch Implementierung der Basisklassen ergänzt werden. Die Factory wählt den Provider anhand der Konfiguration aus.

### Response-Formate
- Vision: `{ "description": "...", "model": "...", "latency_ms": ... }`
- Chat: `{ "answer": "...", "model": "...", "latency_ms": ... }`


## Komponenten

- **Backend:** FastAPI, REST API, SQLite, Embedding- und RAG-Logik, Vision/Chat-Provider
- **Frontend:** React, Upload- und Chat-UI, mobilfähig
- **Uploads:** Speicherung im Backend (uploads/)
- **Datenbank:** SQLite, Tabelle items
- **RAG:** Embedding-Provider, Index, Suche

## Datenfluss

**Upload:**
Frontend → POST /items → Backend speichert Bild, ruft Vision Provider, speichert Beschreibung & Embedding, Antwort an Frontend

**Suche:**
Frontend → POST /search → Backend wandelt Query in Embedding, sucht im Index, gibt Treffer zurück

**Chat:**
Frontend → POST /chat → Backend sucht Kontext, baut Prompt, ruft Chat Provider, Antwort inkl. Trefferliste

## Konfigurationspunkte

- Vision Provider: ENV VISION_PROVIDER
- Chat Provider: ENV CHAT_PROVIDER
- DB-Pfad: fest in backend/app/db/database.py
- Upload-Ordner: backend/uploads/