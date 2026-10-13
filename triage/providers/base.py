"""The one interface every LLM provider must follow.

The classifier only ever calls `classify()`. That is what makes providers
swappable: adding a new vendor means adding one new class here, nothing else.
"""


class LLMProvider:
    name = "base"

    def classify(self, prompt: str) -> str:
        """Send the prompt to the model and return its raw text answer."""
        raise NotImplementedError
