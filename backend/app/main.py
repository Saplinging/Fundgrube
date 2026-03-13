
# --- EINMALIGE, BEREINIGTE IMPLEMENTIERUNG ---
import logging
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from datetime import datetime
import os
from typing import List, Optional
import numpy as np
from app.db.database import SessionLocal, init_db, Item
from sqlalchemy.future import select
from app.llm.factory import get_vision_provider, get_chat_provider
from app.rag.index import DummyEmbeddingProvider, RAGIndex

class Fundstueck(BaseModel):
    id: str
    imageUrl: str
    description: Optional[str] = None
    created_at: datetime
    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    id: str
    description: str | None
    score: float
    imageUrl: str

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]

class ChatResponse(BaseModel):
    answer: str
    matches: list[SearchResult]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

embedding_provider = DummyEmbeddingProvider()
rag_index = RAGIndex()

@app.post("/items", response_model=Fundstueck, status_code=201)
async def upload_item(image: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    max_size = 5 * 1024 * 1024
    if image.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail="Nur jpg, jpeg, png, webp erlaubt.")
    contents = await image.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="Datei zu groß (max 5MB).")
    ext = os.path.splitext(image.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=415, detail="Ungültige Dateiendung.")
    file_id = str(uuid4())
    filename = f"{file_id}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    created = datetime.utcnow()
    description = None
    try:
        vision = get_vision_provider()
        result = vision.describe(file_path)
        description = result.get("description")
    except Exception as e:
        logging.error(f"Vision Provider Fehler: {e}")
        description = None
    embedding = None
    if description:
        embedding = embedding_provider.embed(description)
        rag_index.add(file_id, embedding, model="dummy")
    async with SessionLocal() as session:
        item = Item(id=file_id, image_path=file_path, description=description, created_at=created)
        session.add(item)
        await session.commit()
    return Fundstueck(id=file_id, imageUrl=file_path, description=description, created_at=created)

@app.post("/items/{item_id}/describe", response_model=Fundstueck)
async def regenerate_description(item_id: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        try:
            vision = get_vision_provider()
            result = vision.describe(item.image_path)
            item.description = result.get("description")
            if item.description:
                embedding = embedding_provider.embed(item.description)
                rag_index.update(item.id, embedding, model="dummy")
        except Exception as e:
            logging.error(f"Vision Provider Fehler: {e}")
            item.description = None
        await session.commit()
        return Fundstueck.from_orm(item)

@app.get("/items", response_model=List[Fundstueck])
async def list_items(limit: int = 10, offset: int = 0):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).offset(offset).limit(limit))
        items = result.scalars().all()
        return [Fundstueck.from_orm(i) for i in items]

@app.get("/items/{item_id}", response_model=Fundstueck)
async def get_item(item_id: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Fundstueck.from_orm(item)

@app.post("/rag/reindex")
async def rag_reindex():
    rag_index.clear()
    async with SessionLocal() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        for item in items:
            if item.description:
                embedding = embedding_provider.embed(item.description)
                rag_index.add(item.id, embedding, model="dummy")
    return {"status": "ok", "indexed": len(rag_index.index)}

@app.post("/search", response_model=SearchResponse)
async def search_items(body: dict = Body(...)):
    query = body.get("query")
    top_k = int(body.get("top_k", 5))
    if not query:
        raise HTTPException(status_code=400, detail="query fehlt")
    query_emb = embedding_provider.embed(query)
    results = rag_index.search(query_emb, top_k=top_k)
    items_out = []
    async with SessionLocal() as session:
        for item_id, score in results:
            result = await session.execute(select(Item).where(Item.id == item_id))
            item = result.scalar_one_or_none()
            if item:
                items_out.append(SearchResult(
                    id=item.id,
                    description=item.description,
                    score=score,
                    imageUrl=item.image_path
                ))
    return SearchResponse(query=query, results=items_out)

@app.post("/chat", response_model=ChatResponse)
async def chat_with_rag(body: dict = Body(...)):
    message = body.get("message")
    top_k = int(body.get("top_k", 5))
    if not message:
        raise HTTPException(status_code=400, detail="message fehlt")
    query_emb = embedding_provider.embed(message)
    results = rag_index.search(query_emb, top_k=top_k)
    matches = []
    context_blocks = []
    async with SessionLocal() as session:
        for item_id, score in results:
            result = await session.execute(select(Item).where(Item.id == item_id))
            item = result.scalar_one_or_none()
            if item:
                matches.append(SearchResult(
                    id=item.id,
                    description=item.description,
                    score=score,
                    imageUrl=item.image_path
                ))
                context_blocks.append(f"ID: {item.id}\nBeschreibung: {item.description}")
    system_prompt = "Du bist ein Fundgrube-Experte. Nutze die folgenden Fundstücke, um die Nutzerfrage zu beantworten."
    context = "\n\n".join(context_blocks)
    chat_input = f"{system_prompt}\n\nKontext:\n{context}\n\nNutzer: {message}"
    chat_provider = get_chat_provider()
    chat_result = chat_provider.chat(chat_input)
    return ChatResponse(answer=chat_result['answer'], matches=matches)

@app.post("/items/{item_id}/describe", response_model=Fundstueck)
async def regenerate_description(item_id: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        try:
            vision = get_vision_provider()
            result = vision.describe(item.image_path)
            item.description = result.get("description")
            # Embedding neu erzeugen und Index aktualisieren
            if item.description:
                embedding = embedding_provider.embed(item.description)
                rag_index.update(item.id, embedding, model="dummy")
        except Exception as e:
            logging.error(f"Vision Provider Fehler: {e}")
            item.description = None
        await session.commit()
        return Fundstueck.from_orm(item)

@app.get("/items", response_model=List[Fundstueck])
async def list_items(limit: int = 10, offset: int = 0):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).offset(offset).limit(limit))
        items = result.scalars().all()
        return [Fundstueck.from_orm(i) for i in items]

@app.get("/items/{item_id}", response_model=Fundstueck)
async def get_item(item_id: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Fundstueck.from_orm(item)

@app.post("/rag/reindex")
async def rag_reindex():
    rag_index.clear()
    async with SessionLocal() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        for item in items:
            if item.description:
                embedding = embedding_provider.embed(item.description)
                rag_index.add(item.id, embedding, model="dummy")
    return {"status": "ok", "indexed": len(rag_index.index)}

@app.post("/search", response_model=SearchResponse)
async def search_items(
    body: dict = Body(...)
):
    query = body.get("query")
    top_k = int(body.get("top_k", 5))
    if not query:
        raise HTTPException(status_code=400, detail="query fehlt")
    # ...existing code...

@app.post("/rag/reindex")
async def rag_reindex():
    rag_index.clear()
    async with SessionLocal() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        for item in items:
            if item.description:
                embedding = embedding_provider.embed(item.description)
                rag_index.add(item.id, embedding, model="dummy")
    return {"status": "ok", "indexed": len(rag_index.index)}

@app.get("/items", response_model=List[Fundstueck])
async def list_items(limit: int = 10, offset: int = 0):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).offset(offset).limit(limit))
        items = result.scalars().all()
        return [Fundstueck.from_orm(i) for i in items]

@app.get("/items/{item_id}", response_model=Fundstueck)
async def get_item(item_id: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Fundstueck.from_orm(item)
