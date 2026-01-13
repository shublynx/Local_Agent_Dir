class BaseParser:
    """
    All parsers must implement this interface.
    """

    def parse(self, file_path: str) -> str:
        """
        Takes a file path and returns extracted text.
        """
        raise NotImplementedError
