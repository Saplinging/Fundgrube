import os
import numpy as np
import pickle
from typing import List, Dict, Any

EMBEDDING_DIM = 128  # Dummy dimension
INDEX_PATH = os.path.join(os.path.dirname(__file__), 'index.pkl')

class DummyEmbeddingProvider:
    def embed(self, text: str) -> np.ndarray:
        # Dummy: Hashtext zu Vektor
        np.random.seed(abs(hash(text)) % (2**32))
        return np.random.rand(EMBEDDING_DIM).astype(np.float32)

class RAGIndex:
    def __init__(self):
        self.index: Dict[str, Dict[str, Any]] = {}
        self.load()

    def add(self, item_id: str, embedding: np.ndarray, model: str = "dummy"):
        self.index[item_id] = {
            "embedding": embedding,
            "embedding_model": model
        }
        self.save()

    def update(self, item_id: str, embedding: np.ndarray, model: str = "dummy"):
        self.add(item_id, embedding, model)

    def get(self, item_id: str):
        return self.index.get(item_id)

    def all_items(self):
        return self.index.items()

    def save(self):
        with open(INDEX_PATH, 'wb') as f:
            pickle.dump(self.index, f)

    def load(self):
        if os.path.exists(INDEX_PATH):
            with open(INDEX_PATH, 'rb') as f:
                self.index = pickle.load(f)
        else:
            self.index = {}

    def clear(self):
        self.index = {}
        self.save()

    def search(self, query_emb: np.ndarray, top_k: int = 5):
        results = []
        for item_id, data in self.index.items():
            emb = data["embedding"]
            score = float(np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb)))
            results.append((item_id, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
