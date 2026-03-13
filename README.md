# Fundgrube

Projektstruktur:

- frontend/
- backend/
  - app/
    - llm/
    - rag/
    - db/
    - routes/
- docker/

Dieses Repository enthält die Grundstruktur für das Fundgrube-Projekt.

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


**Provider-System:**
Das Backend unterstützt vollständig austauschbare Provider für Bildbeschreibung und Chat:
- **dummy** (Standard, keine echten KI-Funktionen, keine Kosten)
- **ollama** (lokale LLMs, z.B. Ollama-Server)
- **api** oder **openai** (externe APIs, z.B. OpenAI, Kosten möglich)
Die Auswahl erfolgt über ENV-Variablen (VISION_PROVIDER, CHAT_PROVIDER). Die Provider werden zentral über eine Factory verwaltet – es gibt keine harte Kopplung an Dummy-Provider im Code.

**Hinweis:** Standardmäßig sind Dummy-Provider für Bildbeschreibung und Chat aktiv. Diese erzeugen Testdaten und verursachen keine Kosten.

environment:

**Echte KI-Provider aktivieren:**
Um z.B. OpenAI oder Ollama zu nutzen, stelle die ENV-Variablen wie folgt ein (Beispiele):

Für OpenAI (API):
```
environment:
  - VISION_PROVIDER=api
  - CHAT_PROVIDER=api
  - OPENAI_API_KEY=dein_api_key
```

Für Ollama (lokal):
```
environment:
  - VISION_PROVIDER=ollama
  - CHAT_PROVIDER=ollama
```

Solange VISION_PROVIDER und CHAT_PROVIDER auf "dummy" stehen, entstehen keine Kosten.

## Architekturüberblick

- **Backend:** FastAPI REST API, SQLite DB, Vision- und Chat-Provider austauschbar
- **Frontend:** React + Vite, mobilfähig
- **Uploads:** Bilder werden im Backend gespeichert
- **RAG:** Retrieval über Embeddings, Chat mit Kontext

## Beispielablauf

1. Bild im Frontend hochladen
2. Beschreibung wird automatisch erzeugt
3. Chatfrage stellen, Treffer werden als Kontext genutzt


## LLM Provider wechseln & Kosten

- Die Provider für Bildbeschreibung und Chat werden über ENV-Variablen gesteuert (VISION_PROVIDER, CHAT_PROVIDER).
- Standard ist "dummy" (keine echten KI-Funktionen, keine Kosten).
- Für OpenAI/API muss ein API-Key gesetzt werden (OPENAI_API_KEY). Für Ollama muss ein Ollama-Server laufen.
- Für externe Provider fallen in der Regel Kosten an (siehe Anbieter).
- Die Auswahl und Instanziierung erfolgt modular über eine zentrale Factory (siehe backend/app/llm/factory.py).
- Beispiel-Konfiguration siehe oben und in docker/docker-compose.yaml.
- Weitere Infos: docs/architecture.md

**Weiterentwicklung:**
- Das Provider-System ist jetzt vollständig modular und kann einfach um weitere Provider erweitert werden.
- Dummy-Provider dienen nur zu Test- und Demozwecken.

## API & Details

Siehe docs/api.md und docs/architecture.md