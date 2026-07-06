import os

from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.db = None

    def create_vector_store(self, texts, metadata):

        self.db = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model.model,
            metadatas=metadata
        )

    def save(self, path="faiss_index"):
        self.db.save_local(path)

    def load(self, path="faiss_index"):

        self.db = FAISS.load_local(
            path,
            self.embedding_model.model,
            allow_dangerous_deserialization=True
        )

    def index_exists(self, path="faiss_index"):
        return os.path.exists(path)

    def similarity_search(self, query, k=3):
        return self.db.similarity_search(query, k=k)