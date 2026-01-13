from app.parsers.pdf import PDFParser
from app.parsers.csv_parser import CSVParser
from app.parsers.excel import ExcelParser


def get_parser(file_path: str):
    if file_path.endswith(".pdf"):
        return PDFParser()
    if file_path.endswith(".csv"):
        return CSVParser()
    if file_path.endswith(".xlsx"):
        return ExcelParser()

    raise ValueError("Unsupported file type")
