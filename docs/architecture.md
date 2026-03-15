
# Architektur Fundgrube

## Überblick

Fundgrube ist ein modulares Lost-and-Found System mit automatischer Bildbeschreibung und semantischer Suche per Chat (RAG).

---

## Komponenten

- **Frontend:** React + Vite, Upload- und Chat-UI, mobilfähig
- **Backend:** FastAPI REST API, SQLite DB, Vision/Chat-Provider, Embedding, RAG-Logik
- **Uploads:** Speicherung im Backend (`backend/uploads/`)
- **Datenbank:** SQLite, Tabelle `items` (`backend/app/db/database.py`)
- **RAG:** Embedding-Provider, Index, semantische Suche

---

## Provider-System

- **Vision Provider:** Erzeugt Bildbeschreibungen (dummy, ollama, api/OpenAI)
- **Chat Provider:** Generiert Antworten im Chat (dummy, ollama, api/OpenAI)
- **Provider-Auswahl:**
	- Über ENV-Variablen: `VISION_PROVIDER`, `CHAT_PROVIDER`
	- API-Key für OpenAI: `OPENAI_API_KEY`
	- Ollama-Host: `OLLAMA_HOST` (optional)
- **Factory-Pattern:** Zentrale Auswahl/Instanziierung in `backend/app/llm/factory.py`
- **Erweiterbar:** Neue Provider können einfach ergänzt werden

---

## Datenfluss & Ablauf

```mermaid
flowchart TD
		A[Frontend: Upload-Formular] -->|POST /items| B(Backend: Bild speichern, Vision Provider)
		B -->|Beschreibung & Embedding speichern| C[DB & Index]
		C -->|Antwort mit Beschreibung| A
		D[Frontend: Chat] -->|POST /chat| E(Backend: Suche im Index, Kontext bauen, Chat Provider)
		E -->|Antwort & Treffer| D
		F[Frontend: Suche] -->|POST /search| G(Backend: Suche im Index)
		G -->|Treffer| F
```

---

## ENV-Variablen (Backend)

| Variable           | Beschreibung                                 | Beispielwert           |
|--------------------|----------------------------------------------|------------------------|
| VISION_PROVIDER    | Provider für Bildbeschreibung                | dummy / ollama / api   |
| CHAT_PROVIDER      | Provider für Chat                            | dummy / ollama / api   |
| OPENAI_API_KEY     | API-Key für OpenAI (nur bei Provider=api)    | sk-...                 |
| OLLAMA_HOST        | Host für Ollama-Server (optional)            | http://localhost:11434 |

---

## Response-Formate Provider

- **Vision:** `{ "description": "...", "model": "...", "latency_ms": ... }`
- **Chat:** `{ "answer": "...", "model": "...", "latency_ms": ... }`

---

## Hinweise & Erweiterung

- Die Architektur ist modular, Provider können einfach ergänzt werden.
- Dummy-Provider erzeugen Testdaten (keine Kosten).
- Uploads und Datenbank bleiben nach Neustart erhalten.
- Für API-Details siehe [api.md](api.md)