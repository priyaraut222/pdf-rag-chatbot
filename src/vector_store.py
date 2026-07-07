import os
from langchain_community.vectorstores import FAISS

class VectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.db = None

    def create_vector_store(self, texts, metadata):
        print("Texts:", len(texts))
        print("Metadata:", len(metadata))
        self.db = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model.model,
            metadatas=metadata
        )

    def save(self, path="faiss_index"):
        os.makedirs(path, exist_ok=True)
        self.db.save_local(path)

    def load(self, path="faiss_index"):
        # Explicit reset to wipe previous state out of active memory
        self.db = None 
        self.db = FAISS.load_local(
            path,
            self.embedding_model.model,
            allow_dangerous_deserialization=True
        )

    def index_exists(self, path="faiss_index"):
        return (
            os.path.exists(os.path.join(path, "index.faiss"))
            and
            os.path.exists(os.path.join(path, "index.pkl"))
        )

    def similarity_search(self, query, k=3):
        if not self.db:
            return []
        return self.db.similarity_search(query, k=k)

    def similarity_search_with_score(self, query, k=10):
        if not self.db:
            return []
        return self.db.similarity_search_with_score(query, k=k)