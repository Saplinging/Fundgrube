from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, DateTime
import os

# Datenbankpfad für SQLite im aktuellen Arbeitsverzeichnis (Docker: /app)
DATABASE_URL = "sqlite+aiosqlite:///./fundgrube.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    description = Column(String, nullable=True)
    contact = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
