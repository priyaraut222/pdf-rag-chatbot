from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.db = None

    def create_vector_store(self, chunks):
        self.db = FAISS.from_texts(
            texts=chunks,
            embedding=self.embedding_model.model
        )

    def save(self, path="faiss_index"):
        self.db.save_local(path)

    def load(self, path="faiss_index"):
        self.db = FAISS.load_local(
            path,
            self.embedding_model.model,
            allow_dangerous_deserialization=True
        )

    def similarity_search(self, query, k=3):
        return self.db.similarity_search(query, k=k)