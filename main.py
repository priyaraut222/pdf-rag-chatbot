from src.chat_engine import ChatEngine

engine = ChatEngine()

engine.load_pdfs([
    "data/sample.pdf"
])

question = "Who is the student?"

answer = engine.ask(question)

print(answer)

docs = engine.vector_db.similarity_search(question)

print("\nMetadata:\n")

for doc in docs:
    print(doc.metadata)