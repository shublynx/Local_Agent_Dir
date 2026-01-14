import pandas as pd
from app.parsers.base import BaseParser


class ExcelParser(BaseParser):
    """
    Generic Excel parser:
    - Works for ANY Excel structure
    - One row = one semantic chunk
    - Preserves column meaning
    """

    def parse(self, file_path: str) -> str:
        sheets = pd.read_excel(file_path, sheet_name=None)
        rows = []

        for sheet_name, df in sheets.items():
            # Normalize column names
            df.columns = [str(col).strip() for col in df.columns]

            for _, row in df.iterrows():
                # Build key=value pairs dynamically
                key_values = []

                for col in df.columns:
                    value = row[col]

                    # Skip empty / NaN cells
                    if pd.isna(value):
                        continue

                    key_values.append(f"{col}={value}")

                if key_values:
                    rows.append(
                        f"Sheet={sheet_name} | " + ", ".join(key_values)
                    )

        return "\n".join(rows)
