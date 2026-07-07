import os
from pypdf import PdfReader


class PDFLoader:

    def extract_pages(self, pdf_path, custom_filename=None):
        """
        Extracts text page by page from a PDF.
        Allows a custom_filename override to prevent temporary folder strings from messing up UI metadata.
        """
        reader = PdfReader(pdf_path)
        pages = []

        # Determine the cleanest display name for references
        display_name = custom_filename if custom_filename else os.path.basename(pdf_path)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            # Only collect pages that actually contain readable text layers
            if text and text.strip():
                pages.append(
                    {
                        "text": text,
                        "page": page_number,
                        "source": display_name
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
            "title": metadata.title if metadata and metadata.title else None,
            "author": metadata.author if metadata and metadata.author else None,
            "creator": metadata.creator if metadata and metadata.creator else None,
            "producer": metadata.producer if metadata and metadata.producer else None,
        }