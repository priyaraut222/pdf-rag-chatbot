from src.pdf_loader import PDFLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore


loader = PDFLoader()
text = loader.extract_text("data/sample.pdf")

splitter = TextSplitter()
chunks = splitter.split_text(text)

embedder = EmbeddingModel()

vector_db = VectorStore(embedder)

vector_db.create_vector_store(chunks)

vector_db.save()

print("FAISS index created successfully!")

question = "Who is the student?"

results = vector_db.similarity_search(question)

from src.llm import GeminiLLM

llm = GeminiLLM()

answer = llm.generate_answer(
    question,
    results
)

print("\nAnswer:\n")
print(answer)