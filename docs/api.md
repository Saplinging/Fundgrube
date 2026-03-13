# API Dokumentation

## Health Check
GET /health
Antwort: { "status": "ok" }

## Bild-Upload
POST /items
Input: Multipart Form Data (Feld: file)
Antwort: { id, imageUrl, description, created_at }

## Fundstücke auflisten
GET /items?limit=10&offset=0
Antwort: Liste von Fundstücken

## Fundstück-Details
GET /items/{id}
Antwort: { id, imageUrl, description, created_at }

## Beschreibung neu generieren
POST /items/{id}/describe
Antwort: { id, imageUrl, description, created_at }

## Suche (RAG)
POST /search
Input: { query, top_k }
Antwort: { query, results: [ { id, description, score, imageUrl } ] }

## Chat
POST /chat
Input: { message, top_k }
Antwort: { answer, matches: [ { id, description, score, imageUrl } ] }

## RAG Reindex
POST /rag/reindex
Antwort: { status, indexed }