from pypdf import PdfReader
from app.parsers.base import BaseParser


class PDFParser(BaseParser):

    def parse(self, file_path: str) -> str:
        text = []

        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text)
