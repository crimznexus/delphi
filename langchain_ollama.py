class OllamaEmbeddings:
    def __init__(self, model: str = None):
        self.model = model

    def __call__(self, texts):
        raise RuntimeError(
            "OllamaEmbeddings called but Ollama is not configured in this shim."
        )


class _Resp:
    def __init__(self, content: str):
        self.content = content


class ChatOllama:
    def __init__(self, model: str = "phi3.5", temperature: float = 0.3):
        self.model = model
        self.temperature = temperature

    def invoke(self, prompt: str):
        # Return a simple placeholder response object with `.content`
        return _Resp(
            "Ollama is not configured in this environment. This is a placeholder response."
        )

    def stream(self, prompt: str):
        # Yield a single placeholder chunk to emulate streaming
        yield _Resp(
            "Ollama is not configured in this environment. This is a placeholder response."
        )
