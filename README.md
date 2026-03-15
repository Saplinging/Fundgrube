
# Fundgrube

Fundgrube ist ein modernes **Lost-and-Found System**:

- **Upload von gefundenen Gegenständen** (z.B. Schlüssel, Portemonnaie, etc.)
- **Automatische Bildbeschreibung** durch ein KI-Modell (LLM, z.B. OpenAI oder Ollama)
- **Suche über Chat**: Nutzer können per Chat nach verlorenen Gegenständen suchen (RAG: Retrieval-Augmented Generation)
- **Kontextuelle Trefferanzeige**: Passende Fundstücke werden im Chat als Kontext angezeigt

---

## Projektstruktur

- `frontend/` – React + Vite App (Upload, Chat, UI)
- `backend/`  – FastAPI REST API, SQLite DB, Vision/Chat-Provider, RAG
  - `app/llm/` – Provider für Bildbeschreibung & Chat (dummy, ollama, api)
  - `app/rag/` – Embedding, Index, Suche
  - `app/db/`  – Datenbankmodelle
  - `uploads/`  – Bilder-Uploads
- `docker/`    – Dockerfiles & Compose
- `docs/`      – Architektur, API

---

## Voraussetzungen / Requirements

**Backend:**
- Python >= 3.11
- Empfohlen: venv/virtualenv
- Abhängigkeiten: FastAPI, Uvicorn, SQLAlchemy, aiosqlite, numpy, requests, python-multipart
  (siehe `backend/requirements.txt`)

**Frontend:**
- Node.js >= 20
- npm >= 9
- Abhängigkeiten: React, Vite, TypeScript (siehe `frontend/package.json`)

---

## Environment Variablen (Backend)

| Variable           | Beschreibung                                 | Beispielwert           |
|--------------------|----------------------------------------------|------------------------|
| VISION_PROVIDER    | Provider für Bildbeschreibung                | dummy / ollama / api   |
| CHAT_PROVIDER      | Provider für Chat                            | dummy / ollama / api   |
| EMBEDDING_PROVIDER | Provider für Text-Embeddings (RAG)           | dummy / local / ollama / api / openai |
| OPENAI_API_KEY     | API-Key für OpenAI (nur bei Provider=api)    | sk-...                 |
| OPENAI_EMBEDDING_MODEL | OpenAI Embedding Modell (optional)           | text-embedding-ada-002 |
| OLLAMA_HOST        | Host für Ollama-Server (optional)            | http://localhost:11434 |
| OLLAMA_EMBEDDING_MODEL | Modellname für Ollama Embeddings (optional) | nomic-embed-text       |

**Hinweis:**
- Standardmäßig sind Dummy-Provider aktiv (keine echten KI-Funktionen, keine Kosten).
- Für OpenAI/API muss ein API-Key gesetzt werden. Für Ollama muss ein Ollama-Server laufen.
- Der Embedding-Provider für die RAG-Suche ist jetzt ebenfalls modular und über die ENV-Variable `EMBEDDING_PROVIDER` auswählbar. Standard ist `dummy`. Weitere Provider können einfach ergänzt werden (siehe Code in `backend/app/rag/index.py`).
- Für lokale Embeddings kann `EMBEDDING_PROVIDER=local` gesetzt werden. Es wird dann das Modell `all-MiniLM-L6-v2` von sentence-transformers genutzt (keine Cloud-Kosten, läuft lokal, benötigt aber ausreichend RAM und CPU).

---

## Schnellstart (lokal)

1. Python 3.11+ installieren
2. Im backend-Ordner Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```
3. Backend starten:
   ```
   uvicorn backend.app.main:app --reload
   ```
4. Im frontend-Ordner Abhängigkeiten installieren:
   ```
   npm install
   npm run dev
   ```
5. Frontend läuft auf http://localhost:5173, Backend auf http://localhost:8000

## Schnellstart (Docker)

1. Docker & Docker Compose installieren
2. Im Projektroot:
   ```
   docker compose -f docker/docker-compose.yaml up --build
   ```
3. Frontend: http://localhost:5173  Backend: http://localhost:8000
4. Uploads und Datenbank bleiben nach Neustart erhalten

---

## Demo Walkthrough

1. **Projekt starten** (siehe Schnellstart oben)
2. **Bild hochladen** im Frontend (Seite "Upload")
3. **Automatische Beschreibung** wird durch das Backend erzeugt (LLM)
4. **Chatfrage stellen** (Seite "Chat") – z.B. "Ich habe einen Schlüssel gefunden"
5. **Treffer werden angezeigt**: Passende Fundstücke erscheinen als Kontext im Chat

---


## Architekturüberblick

- **Backend:** FastAPI REST API, SQLite DB, Vision-, Chat- und Embedding-Provider modular
- **Frontend:** React + Vite, mobilfähig
- **Uploads:** Bilder werden im Backend gespeichert
- **RAG:** Retrieval über Embeddings, Chat mit Kontext

**Modularität:**
- Alle Provider (Vision, Chat, Embedding) sind über ENV-Variablen und Factory-Pattern austauschbar.
- Embedding-Provider für die semantische Suche ist in `backend/app/rag/provider.py` und `backend/app/rag/factory.py` implementiert.
- Standard ist ein Dummy-Provider, produktive Provider können einfach ergänzt werden.

Weitere Details: siehe [docs/architecture.md](docs/architecture.md) und [docs/api.md](docs/api.md)

---


## Embedding-Provider (RAG)

- Der Embedding-Provider für die RAG-Suche ist modular und über die ENV-Variable `EMBEDDING_PROVIDER` auswählbar. Standard ist `dummy`.
- Für produktive Nutzung stehen zur Verfügung:
   - `local`: Setze `EMBEDDING_PROVIDER=local` für sentence-transformers (Modell: all-MiniLM-L6-v2, läuft lokal, keine Cloud-Kosten)
   - `ollama`: Setze `EMBEDDING_PROVIDER=ollama`, optional `OLLAMA_EMBEDDING_MODEL` (Standard: `nomic-embed-text`), Ollama-Server muss laufen (`OLLAMA_HOST`)
   - `api`/`openai`: Setze `EMBEDDING_PROVIDER=api` oder `openai`, `OPENAI_API_KEY` muss gesetzt sein, optional `OPENAI_EMBEDDING_MODEL` (Standard: `text-embedding-ada-002`)
- Siehe Code in `backend/app/rag/index.py`.

---


## Beispiel: Lokaler Embedding-Provider

Um lokale Embeddings zu nutzen (ohne Cloud, mit sentence-transformers):

1. Stelle sicher, dass `sentence-transformers` installiert ist (siehe requirements.txt).
2. Setze die Umgebungsvariable:
   ```
   EMBEDDING_PROVIDER=local
   ```
3. Das Modell `all-MiniLM-L6-v2` wird automatisch verwendet.
4. Keine weiteren Einstellungen nötig.

---


## Provider-System & Kosten

- Die Provider für Bildbeschreibung und Chat werden über ENV-Variablen gesteuert (`VISION_PROVIDER`, `CHAT_PROVIDER`).
- Standard ist "dummy" (keine echten KI-Funktionen, keine Kosten).
- Für OpenAI/API muss ein API-Key gesetzt werden (`OPENAI_API_KEY`). Für Ollama muss ein Ollama-Server laufen.
- Für externe Provider können Kosten entstehen (siehe Anbieter).
- Die Auswahl und Instanziierung erfolgt modular über eine zentrale Factory ([backend/app/llm/factory.py](backend/app/llm/factory.py)).
- Beispiel-Konfiguration siehe oben und in [docker/docker-compose.yaml](docker/docker-compose.yaml).

---

## Weiterentwicklung

- Das Provider-System ist modular und kann einfach um weitere Provider erweitert werden.
- Dummy-Provider dienen zu Test- und Demozwecken.

---

## API & Details

Siehe [docs/api.md](docs/api.md) und [docs/architecture.md](docs/architecture.md)