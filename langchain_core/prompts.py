class ChatPromptTemplate:
    def __init__(self, template: str):
        self.template = template

    @classmethod
    def from_template(cls, template: str):
        return cls(template)

    def format(self, **kwargs):
        try:
            return self.template.format(**kwargs)
        except Exception as e:
            # Provide a helpful error if formatting fails
            raise RuntimeError(f"Error formatting prompt template: {e}")
