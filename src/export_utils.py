import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class ChatExporter:

    def __init__(self):

        self.output_folder = "exported"

        os.makedirs(self.output_folder, exist_ok=True)

    def export_chat(self, chat_history):

        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        filepath = os.path.join(
            self.output_folder,
            filename
        )

        doc = SimpleDocTemplate(filepath)

        styles = getSampleStyleSheet()

        story = []

        title = Paragraph(
            "<b>PDF Chatbot Conversation</b>",
            styles["Title"]
        )

        story.append(title)

        story.append(Spacer(1, 20))

        for message in chat_history:

            role = message["role"].capitalize()

            content = message["content"]

            story.append(
                Paragraph(
                    f"<b>{role}:</b> {content}",
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 12)
            )

        doc.build(story)

        return filepath