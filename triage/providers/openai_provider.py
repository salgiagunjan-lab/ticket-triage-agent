"""TODO (Day 2 for OpenAI, Day 4 for the others): implement classify() for this vendor.

Read the API key from the environment (python-dotenv), never hard-code it.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

from triage.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self):
        load_dotenv()  # take environment variables from .env.
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")  
        self.client = OpenAI()
        self.model = os.getenv("OPENAI_MODEL", "gpt-6-luna")  # Default to gpt-6-luna if not set

    def classify(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ], 
            response_format={"type": "json_object"},
            max_completion_tokens=2500
        )
        return response.choices[0].message.content
