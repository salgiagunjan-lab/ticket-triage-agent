"""The one interface every LLM provider must follow.

The classifier only ever calls `classify()`. That is what makes providers
swappable: adding a new vendor means adding one new class here, nothing else.
"""
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod

    def classify(self, prompt: str) -> str:
        """Sends the prompt to the large language model and returns the model’s text answer as is."""
        pass

