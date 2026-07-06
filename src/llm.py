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

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an intelligent PDF Question Answering Assistant.

Rules:

- Answer ONLY from the provided context.
- If the answer is missing, say:
"I couldn't find that information in the uploaded documents."
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

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
Summarize the uploaded documents.

The summary should contain:

• Main topics
• Important information
• Key takeaways

Context:

{context}
"""

        response = self.llm.invoke(prompt)

        return response.content

    # ----------------------------------------------------
    # STUDY NOTES
    # ----------------------------------------------------

    def generate_notes(self, docs):

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
Generate well-structured study notes.

Include:

• Headings
• Bullet Points
• Important Facts
• Revision Notes

Context:

{context}
"""

        response = self.llm.invoke(prompt)

        return response.content

    # ----------------------------------------------------
    # COMPARE PDFs
    # ----------------------------------------------------

    def compare_documents(self, docs):

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
Compare the uploaded PDFs.

Mention:

• Similarities

• Differences

• Important observations

Context:

{context}
"""

        response = self.llm.invoke(prompt)

        return response.content

    # ----------------------------------------------------
    # TRANSLATION
    # ----------------------------------------------------

    def translate(self, text, language):

        prompt = f"""
Translate the following text into {language}.

Text:

{text}
"""

        response = self.llm.invoke(prompt)

        return response.content