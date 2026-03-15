

# Fundgrube API Dokumentation

## Übersicht

REST API für das Lost-and-Found System Fundgrube. Alle Endpunkte liefern JSON.

---

## Provider-System (Modularität)

- Vision-, Chat- und Embedding-Provider sind modular aufgebaut und über ENV-Variablen auswählbar:
	- `VISION_PROVIDER` (dummy/ollama/api)
	- `CHAT_PROVIDER` (dummy/ollama/api)
	- `EMBEDDING_PROVIDER` (dummy / local / ollama / api / openai)
- Die Factory-Pattern-Implementierung findet sich in `app/llm/factory.py` (Vision/Chat) und `app/rag/index.py` (Embedding).
- Standardmäßig ist überall ein Dummy-Provider aktiv. Für lokale Embeddings kann `EMBEDDING_PROVIDER=local` gesetzt werden (Modell: all-MiniLM-L6-v2, sentence-transformers).

## Endpunkte

### 1. Health Check
**GET /health**

Antwort:
```json
{ "status": "ok" }
```

---

### 2. Bild-Upload
**POST /items**

**Input:**
- Multipart Form Data
	- `image` (Datei, Pflichtfeld, jpg/png/webp, max 5MB)
	- `contact` (String, Pflichtfeld)

**Antwort:**
```json
{
	"id": "...",
	"image_path": "...",
	"description": "...", // automatisch generiert
	"contact": "...",
	"created_at": "..."
}
```

**Fehlerfälle:**
- 415: Ungültiger Dateityp/Endung
- 413: Datei zu groß

---

### 3. Fundstücke auflisten
**GET /items?limit=10&offset=0**

Antwort: Array von Fundstücken (wie oben)

---

### 4. Fundstück-Details
**GET /items/{id}**

Antwort: Ein Fundstück (wie oben)

404: Nicht gefunden

---

### 5. Beschreibung neu generieren
**POST /items/{id}/describe**

Antwort: Fundstück mit neuer Beschreibung

404: Nicht gefunden

---

### 6. Suche (RAG)
**POST /search**

**Input:**
```json
{ "query": "Schlüsselbund", "top_k": 5 }
```

**Antwort:**
```json
{
	"query": "Schlüsselbund",
	"results": [
		{ "id": "...", "description": "...", "score": 0.98, "imageUrl": "..." }
	]
}
```

400: query fehlt

---

### 7. Chat mit RAG
**POST /chat**

**Input:**
```json
{ "message": "Ich suche einen Schlüssel", "top_k": 5 }
```

**Antwort:**
```json
{
	"answer": "...", // generierte Antwort
	"matches": [ { "id": "...", "description": "...", "score": 0.97, "imageUrl": "..." } ]
}
```

400: message fehlt

---

### 8. RAG Reindex
**POST /rag/reindex**

Antwort:
```json
{ "status": "ok", "indexed": 42 }
```

---

## Hinweise

- Alle Endpunkte liefern JSON.
- Uploads werden im Backend gespeichert.
- Die Beschreibung wird automatisch durch den gewählten Provider erzeugt.
- Für Details zu Provider/Architektur siehe [architecture.md](architecture.md)