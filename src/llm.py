import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class GeminiLLM:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3,
        )

    # ----------------------------------------------------
    # QUESTION ANSWERING
    # ----------------------------------------------------
    def generate_answer(self, question, docs):
        # Format chunks clearly detailing their individual source files
        context_blocks = []
        for i, doc in enumerate(docs, start=1):
            src = doc.metadata.get("source", "Unknown Document")
            pg = doc.metadata.get("page", "?")
            context_blocks.append(f"--- Chunk {i} | Source: {src} (Page {pg}) ---\n{doc.page_content}")
            
        context = "\n\n".join(context_blocks)

        prompt = f"""
You are an intelligent PDF Question Answering Assistant.

Rules:
- Answer ONLY from the provided context.
- If the answer is missing, say: "I couldn't find that information in the uploaded documents."
- Keep answers concise.
- Use bullet points whenever appropriate.

Context:
{context}

Question:
{question}

Answer:
"""
        response = self.llm.invoke(prompt)
        return response.content

    # ----------------------------------------------------
    # PDF SUMMARY
    # ----------------------------------------------------
    def summarize_documents(self, docs):
        # Group page content chunks by their unique file names
        grouped_docs = {}
        for doc in docs:
            src = doc.metadata.get("source", "Unknown Document")
            if src not in grouped_docs:
                grouped_docs[src] = []
            grouped_docs[src].append(doc.page_content)

        # Structure context so each file summary is clearly isolated
        context_str = ""
        for filename, chunks in grouped_docs.items():
            context_str += f"\n\n==================== DOCUMENT: {filename} ====================\n"
            context_str += "\n".join(chunks)

        prompt = f"""
Summarize the uploaded documents. 
You must provide a distinct summary section for EACH individual file present in the context below. Do not group them into one generic summary.

The summary should contain:
• Main topics
• Important information
• Key takeaways

Context:
{context_str}
"""
        response = self.llm.invoke(prompt)
        return response.content

    # ----------------------------------------------------
    # STUDY NOTES
    # ----------------------------------------------------
    def generate_notes(self, docs):
        grouped_docs = {}
        for doc in docs:
            src = doc.metadata.get("source", "Unknown Document")
            if src not in grouped_docs:
                grouped_docs[src] = []
            grouped_docs[src].append(doc.page_content)

        context_str = ""
        for filename, chunks in grouped_docs.items():
            context_str += f"\n\n--- Start of Material: {filename} ---\n"
            context_str += "\n".join(chunks)

        prompt = f"""
Generate well-structured study notes from the context material below. 
Organize the breakdown into clean sections, clearly calling out references to the source file names.

Include:
• Headings
• Bullet Points
• Important Facts
• Revision Notes

Context:
{context_str}
"""
        response = self.llm.invoke(prompt)
        return response.content

    # ----------------------------------------------------
    # COMPARE PDFs
    # ----------------------------------------------------
    def compare_documents(self, docs):
        # CRITICAL FIX: Explicitly separate chunks into containers by filename
        grouped_docs = {}
        for doc in docs:
            src = doc.metadata.get("source", "Unknown Document")
            if src not in grouped_docs:
                grouped_docs[src] = []
            grouped_docs[src].append(doc.page_content)

        context_str = ""
        for filename, chunks in grouped_docs.items():
            context_str += f"\n\n📦 FILE STRUCTURE CONTAINER: {filename}\n"
            context_str += "\n".join(chunks)
            context_str += f"\n📦 END OF CONTAINER: {filename}\n"

        prompt = f"""
Compare the uploaded PDFs. You have been provided multiple distinct documents wrapped in explicit file containers.
Run a deep cross-comparative analysis contrasting these distinct files against each other.

Mention:
• Similarities (shared components, matching concepts)
• Differences (what file A includes that file B completely misses or contradicts)
• Important observations

Context:
{context_str}
"""
        response = self.llm.invoke(prompt)
        return response.content

    # ----------------------------------------------------
    # TRANSLATION
    # ----------------------------------------------------
    def translate(self, text, language):
        prompt = f"""
Translate the following text into {language}. Keep any Markdown format styles completely intact.

Text:
{text}
"""
        response = self.llm.invoke(prompt)
        return response.content