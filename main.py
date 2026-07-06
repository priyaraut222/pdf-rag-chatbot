from src.chat_engine import ChatEngine

engine = ChatEngine()

engine.load_pdf("data/sample.pdf")

question = "Who is the student?"

answer = engine.ask(question)

print(answer)