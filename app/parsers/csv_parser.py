import pandas as pd
from app.parsers.base import BaseParser


class CSVParser(BaseParser):

    def parse(self, file_path: str) -> str:
        df = pd.read_csv(file_path)

        # Convert rows into readable text
        return df.to_string(index=False)
