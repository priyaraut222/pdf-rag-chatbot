import os

from pypdf import PdfReader


class PDFLoader:

    def extract_pages(self, pdf_path):

        reader = PdfReader(pdf_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text and text.strip():

                pages.append(
                    {
                        "text": text,
                        "page": page_number,
                        "source": os.path.basename(pdf_path)
                    }
                )

        return pages

    # ------------------------------------------------------
    # Optional helper
    # ------------------------------------------------------

    def extract_text(self, pdf_path):

        pages = self.extract_pages(pdf_path)

        return "\n".join(
            page["text"] for page in pages
        )

    # ------------------------------------------------------
    # Get total pages
    # ------------------------------------------------------

    def get_total_pages(self, pdf_path):

        reader = PdfReader(pdf_path)

        return len(reader.pages)

    # ------------------------------------------------------
    # PDF Information
    # ------------------------------------------------------

    def get_pdf_info(self, pdf_path):

        reader = PdfReader(pdf_path)

        metadata = reader.metadata

        return {
            "filename": os.path.basename(pdf_path),
            "pages": len(reader.pages),
            "title": metadata.title if metadata else None,
            "author": metadata.author if metadata else None,
            "creator": metadata.creator if metadata else None,
            "producer": metadata.producer if metadata else None,
        }