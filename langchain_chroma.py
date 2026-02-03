import os
import pickle
from typing import List, Tuple

# Simple persistent storage for 'documents'. Documents are expected to have
# a `page_content` attribute and optional `metadata` mapping.

class Chroma:
    def __init__(self, persist_directory: str = None, embedding_function=None):
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self._docs = []
        if persist_directory and os.path.exists(persist_directory):
            try:
                with open(os.path.join(persist_directory, "documents.pickle"), "rb") as f:
                    self._docs = pickle.load(f)
            except Exception:
                self._docs = []

    @classmethod
    def from_documents(cls, documents: List[object], embedding=None, persist_directory: str = None):
        instance = cls(persist_directory=persist_directory, embedding_function=embedding)
        instance._docs = list(documents)
        if persist_directory:
            os.makedirs(persist_directory, exist_ok=True)
            with open(os.path.join(persist_directory, "documents.pickle"), "wb") as f:
                pickle.dump(instance._docs, f)
        return instance

    def similarity_search(self, query: str, k: int = 5) -> List[object]:
        scored = self._score_docs(query)
        return [doc for doc, _ in scored[:k]]

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[object, float]]:
        scored = self._score_docs(query)
        return scored[:k]

    def _score_docs(self, query: str):
        if not self._docs:
            return []
        q_words = [w.lower() for w in query.split() if w.strip()]
        scored = []
        for doc in self._docs:
            text = getattr(doc, "page_content", "") or ""
            text_low = text.lower()
            score = sum(text_low.count(w) for w in q_words)
            scored.append((doc, float(score)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
