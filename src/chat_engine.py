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

        self.loaded_documents = []

    # --------------------------------------------------
    # Load PDFs
    # --------------------------------------------------

    def load_pdfs(self, pdf_paths):

        if self.vector_db.index_exists():

            print("Loading existing FAISS index...")

            self.vector_db.load()

            self.loaded_documents = pdf_paths

            return

        print("Creating new FAISS index...")

        all_texts = []
        all_metadata = []

        for pdf in pdf_paths:

            pages = self.loader.extract_pages(pdf)

            for page in pages:

                chunks = self.splitter.split_text(
                    page["text"]
                )

                for chunk in chunks:

                    all_texts.append(chunk)

                    all_metadata.append(
                        {
                            "source": page["source"],
                            "page": page["page"]
                        }
                    )

        self.vector_db.create_vector_store(
            all_texts,
            all_metadata
        )

        self.vector_db.save()

        self.loaded_documents = pdf_paths

    # --------------------------------------------------
    # Question Answering
    # --------------------------------------------------

    def ask(self, question):

        docs = self.vector_db.similarity_search(
            question
        )

        answer = self.llm.generate_answer(
            question,
            docs
        )

        return {
            "answer": answer,
            "sources": docs
        }

    # --------------------------------------------------
    # Summarize PDFs
    # --------------------------------------------------

    def summarize(self):

        docs = self.vector_db.similarity_search(
            "Provide a complete summary of all uploaded documents.",
            k=20
        )

        return self.llm.summarize_documents(docs)

    # --------------------------------------------------
    # Generate Notes
    # --------------------------------------------------

    def generate_notes(self):

        docs = self.vector_db.similarity_search(
            "Generate detailed study notes.",
            k=20
        )

        return self.llm.generate_notes(docs)

    # --------------------------------------------------
    # Compare PDFs
    # --------------------------------------------------

    def compare_pdfs(self):

        docs = self.vector_db.similarity_search(
            "Compare all uploaded PDFs. Mention similarities and differences.",
            k=20
        )

        return self.llm.compare_documents(docs)

    # --------------------------------------------------
    # Translate
    # --------------------------------------------------

    def translate_answer(
        self,
        answer,
        language
    ):

        if language == "English":
            return answer

        return self.llm.translate(
            answer,
            language
        )