from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:

    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, chunks):
        return self.model.embed_documents(chunks)

    def embed_query(self, question):
        return self.model.embed_query(question)