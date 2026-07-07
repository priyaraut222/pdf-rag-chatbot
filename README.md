# 🤖 ChatPDF AI — Advanced Multi-PDF RAG Analytics Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-121212?logo=chainlink&logoColor=white)](https://github.com/langchain-ai/langchain)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-0091FF?logo=googlegemini&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![VectorDB](https://img.shields.io/badge/Vector%20Store-FAISS-76B900?logo=nvidia&logoColor=white)](https://github.com/facebookresearch/faiss)

An enterprise-grade **Retrieval-Augmented Generation (RAG)** system built to perform semantic searches, contextual Q&A, and cross-document comparative workflows across multiple complex PDF structures simultaneously. Featuring a highly optimized processing backend, context-preserving text partitioning, and a premium UI workspace.

---

## 🚀 Key Production Features

* **🎙️ Multi-Modal Voice Inputs (`mic_recorder`):** Seamlessly dictate voice prompts directly into the workspace. Queries are transcribed with high temporal alignment and automatically processed by the reasoning engine.
* **⚖️ Dynamic Multi-Document Cross-Comparison:** Breaks down data silos. The engine groups distinct files into explicit source-tracking boundaries, enabling the LLM to contrast parameters, target structural contradictions, and discover discrepancies across multiple documents simultaneously.
* **📂 Isolated AI Workspaces:** A functional task abstraction selector allows switching between distinct workflow states instantly:
    * `💬 Chat with PDFs` (Granular Source-Authenticated QA)
    * `📄 Summarize PDFs` (Independent Deep Document Profiles)
    * `📝 Generate Study Notes` (Structured Knowledge Graph Transcripts)
    * `⚖️ Compare PDFs` (Cross-pollinated Relational Analytics Matrix)
* **⚡ Sub-Millisecond Vector Ingestion & Local Caching:** Powered by Facebook AI Similarity Search (**FAISS**). Documents are mapped dynamically using customized cryptographic filename hashes to bypass dirty application cache hits.
* **🌐 Language Localization Matrix:** On-the-fly translation layers shift UI context responses into multiple global languages while preserving strict markdown structures.
* **🎨 Premium UI / UX Interface:** A dark-mode optimized canvas built with professional layout design, interactive action components, and instant real-time side-bar indexing state tracking.

---

## 🏗️ Architectural Topography & System Flow

The platform relies on a modular OOP pattern isolating processing state steps to prevent frame-refresh performance loops in Streamlit:

```text
📥 User Uploads Multi-PDFs 
    │
    ├──► 🧩 src/pdf_loader.py ──► PyPDF Text Layer Extraction (Zero Metadata Leakage)
    │
    ├──► ✂️ src/text_splitter.py ─► Dynamic Text Overlap Windows & Structural Token Chunking
    │
    ├──► 🧬 src/embeddings.py ───► Content Dense Vectorization Matrix Mapping
    │
    └──► 🗄️ src/vector_store.py ─► Cryptographic Cache Lookup ──► Saved FAISS Local Shards (.faiss + .pkl)
            │
            ▼ 
🔍 Semantic Similarity Search Engine (k=10 Document Intersection)
            │
            ▼
🧠 src/llm.py (ChatGoogleGenerativeAI Engine Running Context-Tagged Content Formats)
            │
            ▼
💻 Streamlit Premium Interface Output Workspace Rendering Engine

🛠️ Tech Stack & Technical Blueprint
Core Orchestration: LangChain (LangChain-Core, LangChain-Community)

Intelligence Layer: Google GenAI / langchain-google-genai (Model: gemini-2.5-flash)

High-Performance Indexing: FAISS (Facebook AI Similarity Search)

File Deserialization Engine: PyPDF / pypdf (Native coordinate text bounds recovery)

Runtime Environment: Streamlit web framework + Python .env configuration pattern

📦 File Layout Matrix

pdf-rag-chatbot/
├── .env                  # Protected API Credentials Configuration
├── app.py                # Main Streamlit Graphical Application Workspace
├── requirements.txt      # System Level Core Dependencies Matrix
├── indexes/              # Encrypted Session Vector Document Databases
└── src/                  # Object Oriented Backend Engineering Directory
    ├── __init__.py
    ├── chat_engine.py    # Main Coordination, State Synchronization & Route Management
    ├── embeddings.py     # Content Dense Vectorization Ingestion Wrapper
    ├── llm.py            # Context-Aware Isolated Prompt & Structural Completion Engine
    ├── pdf_loader.py     # Native IO Document Character Vector Extractors
    ├── text_splitter.py  # Token Boundary Tokenizers & Document Content Chunkers
    └── vector_store.py   # Local Database Persistence & High Precision k-NN Retrievers
