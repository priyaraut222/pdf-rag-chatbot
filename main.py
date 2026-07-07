from src.chat_engine import ChatEngine
from src.export_utils import ChatExporter

# =====================================================
# INITIALIZE
# =====================================================

engine = ChatEngine()

exporter = ChatExporter()

# =====================================================
# LOAD PDF(s)
# =====================================================

engine.load_pdfs(
    [
        "data/sample.pdf"
    ]
)

print("\n✅ PDFs Loaded Successfully!\n")

# =====================================================
# ASK QUESTION
# =====================================================

question = input("Ask a question: ")

result = engine.ask(question)

print("\n========== ANSWER ==========\n")

print(result["answer"])

# =====================================================
# SOURCES
# =====================================================

print("\n========== SOURCES ==========\n")

for doc in result["sources"]:

    print(
        f"📄 {doc.metadata['source']} | Page {doc.metadata['page']}"
    )

# =====================================================
# EXPORT CHAT
# =====================================================

history = [
    {
        "role": "user",
        "content": question
    },
    {
        "role": "assistant",
        "content": result["answer"]
    }
]

pdf_path = exporter.export_chat(history)

print("\n========== CHAT EXPORTED ==========\n")

print(pdf_path)