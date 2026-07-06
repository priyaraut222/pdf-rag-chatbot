from src.pdf_loader import PDFLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingModel

loader = PDFLoader()

text = loader.extract_text("data/sample.pdf")

splitter = TextSplitter()

chunks = splitter.split_text(text)

embedder = EmbeddingModel()

embeddings = embedder.embed_documents(chunks)

print(f"Total chunks: {len(chunks)}")

print(f"Embedding dimension: {len(embeddings[0])}")

print(embeddings[0][:10])