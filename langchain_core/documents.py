class BaseDocument(dict):
    """Minimal document class that supports page_content and metadata."""
    def __init__(self, page_content: str = "", metadata: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.page_content = page_content
        self.metadata = metadata or {}


class Document(BaseDocument):
    """Alias to BaseDocument for compatibility."""
    pass
