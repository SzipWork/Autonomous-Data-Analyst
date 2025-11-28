# app/database/vector_db.py
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except Exception:
    CHROMADB_AVAILABLE = False


class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self._store = {}

        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(
                    path=persist_directory,
                    settings=Settings(anonymized_telemetry=False)
                )

                self.collection = self.client.get_or_create_collection(
                    name="data_memory",
                    metadata={"hnsw:space": "cosine"},
                    embedding_function=None
                )
            except Exception:
                self._fallback_init()
        else:
            self._fallback_init()

    def _fallback_init(self):
        self._store = {}

    def add_context(self, dataset_name: str, text: str):
        doc_id = f"{dataset_name}_{datetime.now().timestamp()}"
        meta = {"dataset": dataset_name, "timestamp": datetime.now().isoformat()}

        if CHROMADB_AVAILABLE and hasattr(self, "collection"):
            try:
                self.collection.add(
                    ids=[doc_id],
                    documents=[text],
                    metadatas=[meta]
                )
                return doc_id
            except Exception:
                pass

        self._store[doc_id] = {"text": text, "metadata": meta}
        return doc_id

    def search(self, query: str, limit: int = 5):
        if CHROMADB_AVAILABLE and hasattr(self, "collection"):
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=limit
                )
                docs = results["documents"][0]
                return docs
            except Exception:
                pass

        return [
            item["text"]
            for item in self._store.values()
            if query.lower() in item["text"].lower()
        ][:limit]
