import pandas as pd
from app.parsers.base import BaseParser


class ExcelParser(BaseParser):

    def parse(self, file_path: str) -> str:
        sheets = pd.read_excel(file_path, sheet_name=None)

        text_blocks = []

        for sheet_name, df in sheets.items():
            text_blocks.append(f"Sheet: {sheet_name}")
            text_blocks.append(df.to_string(index=False))

        return "\n\n".join(text_blocks)
