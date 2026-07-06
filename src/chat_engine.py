from src.pdf_loader import PDFLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.llm import GeminiLLM


class ChatEngine:

    def __init__(self):

        self.loader = PDFLoader()
        self.splitter = TextSplitter()
        self.embedder = EmbeddingModel()
        self.vector_db = VectorStore(self.embedder)
        self.llm = GeminiLLM()

    def load_pdf(self, pdf_path):

        text = self.loader.extract_text(pdf_path)

        chunks = self.splitter.split_text(text)

        self.vector_db.create_vector_store(chunks)

        self.vector_db.save()

    def ask(self, question):

        docs = self.vector_db.similarity_search(question)

        answer = self.llm.generate_answer(
            question,
            docs
        )

        return answer