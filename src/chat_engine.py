import hashlib
import os
from langchain_core.documents import Document
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
        self.vectordb = VectorStore(self.embedder)
        self.llm = GeminiLLM()
        self.loaded_documents = []
        self.all_docs = []

    def get_index_path(self, pdf_paths):
        # FIX: Base the hash folder on actual filenames, NOT changing temp directory paths
        normalized_names = [os.path.basename(p) for p in pdf_paths]
        pdf_string = "".join(sorted(normalized_names))
        pdf_hash = hashlib.md5(pdf_string.encode()).hexdigest()
        return os.path.join("indexes", pdf_hash)

    def load_pdfs(self, pdf_paths):
        index_path = self.get_index_path(pdf_paths)
        
        # ALWAYS scrub active memory state on every new file upload action
        self.all_docs = []
        self.loaded_documents = pdf_paths

        # Re-build document cache objects instantly
        all_texts, all_metadata = self._build_document_cache(pdf_paths)

        if self.vectordb.index_exists(index_path):
            print("Loading matched cached FAISS index structure...")
            self.vectordb.load(index_path)
            return

        print("Creating completely new FAISS matrix structure...")
        print("Total Chunks:", len(all_texts))
        
        self.vectordb.create_vector_store(all_texts, all_metadata)
        self.vectordb.save(index_path)

    def _build_document_cache(self, pdf_paths):
        all_texts = []
        all_metadata = []
        
        for pdf in pdf_paths:
            actual_filename = os.path.basename(pdf)
            pages = self.loader.extract_pages(pdf)
            
            for page in pages:
                chunks = self.splitter.split_text(page["text"])
                for chunk in chunks:
                    all_texts.append(chunk)
                    
                    metadata = {
                        "source": actual_filename,
                        "page": page.get("page", 1)
                    }
                    all_metadata.append(metadata)
                    
                    # FIX: Explicitly bundle the document context title inside the layout string 
                    # so Gemini is forced to realize multiple documents are present.
                    self.all_docs.append(
                        Document(
                            page_content=f"--- START OF FILE: {actual_filename} (Page {page.get('page', 1)}) ---\n{chunk}\n--- END OF FILE Reference ---",
                            metadata=metadata
                        )
                    )
        return all_texts, all_metadata

    def ask(self, question):
        # Retrieve top 10 chunks to ensure cross-pollination between multiple PDFs
        docs = self.vectordb.similarity_search(question, k=10)
        
        print("\n========== RETRIEVED DOCS ==========\n")
        for doc in docs:
            print(doc.metadata)
            
        answer = self.llm.generate_answer(question, docs)
        return {"answer": answer, "sources": docs}  

    def summarize(self):
        if not self.all_docs:
            return "No documents loaded to summarize."
        return self.llm.summarize_documents(self.all_docs)

    def generate_notes(self):
        if not self.all_docs:
            return "No documents loaded to generate notes."
        return self.llm.generate_notes(self.all_docs)

    def compare_pdfs(self):
        if not self.all_docs:
            return "No documents loaded to compare."
        return self.llm.compare_documents(self.all_docs)

    def translate_answer(self, answer, language):
        if language == "English":
            return answer
        return self.llm.translate(answer, language)