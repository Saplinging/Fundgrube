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

**Hinweis:** Standardmäßig sind Dummy-Provider für Bildbeschreibung und Chat aktiv. Diese erzeugen Testdaten und verursachen keine Kosten.

**Echte KI-Provider:**
Um z.B. OpenAI oder andere Modelle zu nutzen, muss ein passender Provider im Backend implementiert und per ENV-Variable aktiviert werden. Für die Nutzung externer APIs entstehen in der Regel Kosten (siehe jeweiliger Anbieter). Beispiel für Docker Compose:

```
environment:
  - VISION_PROVIDER=openai
  - CHAT_PROVIDER=openai
  - OPENAI_API_KEY=dein_api_key
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

## LLM Provider wechseln

## LLM Provider wechseln und Kosten

- Die Provider für Bildbeschreibung und Chat werden über ENV-Variablen gesteuert (VISION_PROVIDER, CHAT_PROVIDER).
- Standard ist "dummy" (keine echten KI-Funktionen, keine Kosten).
- Für echte Provider (z.B. OpenAI) muss ein passender Provider im Backend vorhanden sein und ein API-Key gesetzt werden.
- Für externe Provider fallen in der Regel Kosten an (siehe Anbieter).
- Beispiel-Konfiguration siehe oben und in docker/docker-compose.yaml.
- Weitere Infos: docs/architecture.md

**Weiterentwicklung:**
- Für produktive KI-Funktionen müssen echte Provider implementiert und konfiguriert werden.
- Dummy-Provider dienen nur zu Test- und Demozwecken.

## API & Details

Siehe docs/api.md und docs/architecture.md